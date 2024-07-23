from Constants import VHDL_LIBRARIES, VHDL_LIBRARY_DECLARATION
from Component import Component
from Gate import LSTM_Unit
from Num2Bin import Num2Bin, Bin2Num

class Communication(Component):
    """Middle interface between FPGA and MCU
       - Receives inputs
       - Converts binary inputs to integers
       - Receives inputs until all inputs are ready
       - Passes input array to LSTM_Unit to perform inference
       - Converts inferred result to bin and for microcontroller to read
    """
    def __init__(self, nbits, forget_data, input_data, candidate_data, output_data, n_inputs, input_shape, weight_shape):
        self.nbits = nbits
        self.weight_shape = weight_shape
        self.n_inputs = n_inputs
        self.input_shape = input_shape
        self.input_data = input_data
        self.candidate_data = candidate_data
        self.output_data = output_data
        self.forget_data = forget_data

    @property
    def name(self):
        return 'communication_module'
        
    def getEntity(self):
        return f"""
        entity {self.name} is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                rst    : in std_logic;
                ctrl   : in std_logic_vector(1 downto 0);
                inbits : in std_logic_vector({self.nbits-1} downto 0);
                outbits: out std_logic_vector({self.nbits-1} downto 0)
                );
        end {self.name};
        """
    
    def getComponent(self):
        return f"""
        component {self.name} is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                rst    : in std_logic;
                ctrl   : in std_logic_vector(1 downto 0);
                inbits : in std_logic_vector({self.nbits-1} downto 0);
                outbits: out std_logic_vector({self.nbits-1} downto 0)
                );
        end component;
        """
    
    def getInstance(self, clk, EN, rst, ctrl, inbits, outbits):
        return f"""
        {self.name}_inst: {self.name} port map(
            clk     => {clk},
            EN      => {EN},
            rst     => {rst},
            ctrl    => {ctrl},
            inbits  => {inbits},
            outbits => {outbits}
        );
        """
    
    def toVHDL(self):
        lstm_unit = LSTM_Unit(self.forget_data, self.input_data, self.candidate_data, self.output_data, self.n_inputs, self.input_shape, self.weight_shape)
        num2bin   = Num2Bin(self.nbits)
        input_picker = Input_Picker(self.nbits)

        lstm_unit.writeToFle()
        num2bin.writeToFle()
        input_picker.writeToFle()

        return f"""
        {VHDL_LIBRARIES}
        {VHDL_LIBRARY_DECLARATION}
        {self.getEntity()}

        architecture Behavioral of {self.name} is
        {lstm_unit.getComponent()}
        {num2bin.getComponent()}
        {input_picker.getComponent()}

        -- relevant signals
        signal input_arr 	   	 : input_array;

        signal lstm_unit_pre_en  : std_logic;
        signal lstm_en    	     : std_logic;
        signal lstm_unit_done  	 : std_logic;

        signal bin2num_en      	 : std_logic;
        signal num2bin_pre_en	 : std_logic;
        signal num2bin_en	  	 : std_logic;
        signal bin2num_done    	 : std_logic; -- not really necessary here, should go in input_picker
        signal num2bin_done      : std_logic;
        signal inputs_ready    	 : std_logic;

        signal input_picker_en	 : std_logic;
        signal input_picker_done : std_logic;

        signal tmp_num 			 : integer;

        signal output 			 : integer;
        signal sum_done			 : std_logic;

        begin
            process(clk)
            begin
                -- reset is done on mcu side.
                -- if you reset, set ctrl_signal to idle too
                
                if rst = '1' then
                    null;
                else
                    if rising_edge(clk) then
                        if en = '1' then
                            case ctrl is
                                -- idle: just maintain signals
                                when "00" => 
                                    null;

                                -- recv input
                                when "01" => 
                                    lstm_unit_pre_en  <= '0';
                                    input_picker_en   <= '1';
                                    num2bin_pre_en    <= '0';

                                -- run inference happens when inputs are ready
                                when "10" => 
                                    lstm_unit_pre_en  <= '1';
                                    num2bin_pre_en    <= '0';
                                    input_picker_en   <= '0';

                                -- output result convert num to bin and send to appropriate pins then maintain signal with idle
                                when "11" => 
                                    lstm_unit_pre_en  <= '0';
                                    num2bin_pre_en    <= '1';
                                    input_picker_en   <= '0';

                                when others =>
                                    lstm_unit_pre_en  <= '0';
                                    num2bin_pre_en 	  <= '0';
                                    input_picker_en   <= '0';
                            end case;
                        end if;
                    end if;
                end if;  
            end process;
    
            inputs_ready_infer : process (clk)
            begin
                if rising_edge(clk) then
                    if en = '1' then
                        if input_picker_done = '1' and lstm_unit_pre_en = '1' then
                            lstm_en <= '1';
                        end if;
                    end if;
                end if;
            end process;

            {input_picker.getInstance('clk', 'input_picker_en', 'inbits', 'input_arr', 'input_picker_done')}
            {lstm_unit.getInstance('clk', 'lstm_en', 'input_arr', 'output', 'lstm_unit_done')}
   
            output_ready_generate_bits : process(clk)
            begin
                if rising_edge(clk) then
                    if en = '1' then
                        if num2bin_pre_en = '1' and lstm_unit_done = '1' then
                            num2bin_en <= '1';
                        end if;
                    end if;
                end if;
            end process;

            {num2bin.getInstance('clk', 'num2bin_en', 'output', 'outbits', 'num2bin_done')}
        end behavioral;
        """



class Input_Picker(Component):
    """Stores inputs from MCU until they are all ready to be passed to model"""

    def __init__(self, nbits):
        self.nbits = nbits

    @property
    def name(self):
        return 'input_picker'
    
    def getEntity(self):
        return f"""
        entity {self.name} is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                inbits : in std_logic_vector({self.nbits-1} downto 0);
                output : out input_array;
                done   : out std_logic
            );
        end {self.name};
        """
    
    def getComponent(self):
        return f"""
        component {self.name} is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                inbits : in std_logic_vector({self.nbits-1} downto 0);
                output : out input_array;
                done   : out std_logic
            );
        end component;
        """
    
    def getInstance(self, clk, EN, inbits, output, done):
        return f"""
        {self.name}_inst: {self.name} port map(
            clk    => {clk},
            EN     => {EN},
            inbits => {inbits},
            output => {output},
            done   => {done}
        );
        """
    
    def toVHDL(self):
        bin2num = Bin2Num(self.nbits)
        bin2num.writeToFle()

        return f"""
        {VHDL_LIBRARIES}
        {VHDL_LIBRARY_DECLARATION}
        {self.getEntity()}

        architecture Behavioral of {self.name} is
        {bin2num.getComponent()}
            signal index : integer := 0;
            signal all_in : std_logic := '0';
            signal num : integer;
            signal bin2num_done : std_logic;

            begin
                {bin2num.getInstance('clk', 'en', 'num', 'inbits', 'bin2num_done')}
                process(clk)
                begin
                    if rising_edge(clk) then
                        if en = '1' and all_in = '0' and num > -2147483648 then
                            output(index) <= num;
                            index <= index + 1;
                            if index = output'length-1 then
                                done <= '1';
                                all_in <= '1';
                            else
                                done <= '0';
                            end if;
                        end if;
                    end if;
                end process;
        end behavioral;
        """
    
if __name__ == "__main__":
    data = [
{'input_weights': 1048, 'gate_biases': 993998, 'short_weights': 667},
{'input_weights': -1187, 'gate_biases': 489871, 'short_weights': 777},
{'input_weights': 869, 'gate_biases': -256319, 'short_weights': 1194},
{'input_weights': 1297, 'gate_biases': 548073, 'short_weights': 235}]
    nbits = 10
    comms = Communication(nbits, data[0], data[2], data[1], data[3], 4, [1, 1], [1, 1])
    comms.writeToFle()