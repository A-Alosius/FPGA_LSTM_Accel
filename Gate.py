from Constants import VHDL_LIBRARIES, VHDL_LIBRARY_DECLARATION
from Component import Component
from Activation import Sigmoid, Tanh, Activate_Vector
from Arithmetic import MatrixMultiplier, Adder, HigherBiasAdder, Multiplier, ElementWiseMultiplier
from Config_generator import Configuration

matmul = MatrixMultiplier()
elmul = ElementWiseMultiplier()
mul = Multiplier()
add = Adder()
hadder = HigherBiasAdder()
sig = Sigmoid()
tanh = Tanh()

class Gate(Component):
    def __init__(self, gate:str, input_weights, gate_biases, short_weights, activation:str):
        self.gate = gate
        self.input_weights = input_weights
        self.gate_biases = gate_biases
        self.short_weights = short_weights
        self.activation = activation

    @property
    def name(self)->str:
        return f'{self.gate}'
    
    def values(self, input, label):
        output_string = ''
        if (type(input) == int):
            output_string += str(input)
        elif type(input) == list:
            if type(input[0]) == int:
                output_string += f'{label}(0) <= ('
                for k, i in enumerate(input):
                    print(i)
                    output_string += str(i)
                    if k == len(input)-1:
                        break
                    output_string += ", "
                output_string += ');'

            elif type(input[0]) == list:
                for k, i in enumerate(input):
                    print(k)
                    output_string += f'{label}({k}) <= ('
                    for inner, j in enumerate(i):
                        output_string += str(j)
                        if inner == len(i)-1:
                            break
                        output_string += ", "
                    output_string += ');\n'
        return output_string

    def getEntity(self) -> str:
        return f"""
        entity {self.name} is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                input         : in output_type;
                short         : in output_type;
                output        : out output_type;
                done          : out std_logic
            );

            -- declare and instantiate weight and biases for each gate here
            signal input_weights : weight_type{':= ' + self.values(self.input_weights, '') if type(self.input_weights) == int else ''};
            signal gate_biases   : output_type{':= ' + self.values(self.gate_biases, '') if type(self.gate_biases) == int else ''};
            signal short_weights : weight_type{':= ' + self.values(self.short_weights, '') if type(self.short_weights) == int else ''};
        end entity {self.name};
        """

    def getComponent(self)->str:    
        return f"""
        component {self.name} is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                input         : in output_type;
                short         : in output_type;
                output        : out output_type;
                done          : out std_logic
            );
        end component;
        """
    
    def getInstance(self, clk, EN, input, short, output, done) -> str:
        return f"""
        {self.name}_inst: {self.name} port map(
            clk          => {clk},
            EN           => {EN},
            input        => {input},
            short        => {short},
            output       => {output},
            done         => {done}
        );
        """
    
    def toVHDL(self) -> str:
        tanh.writeToFle()
        sig.writeToFle()
        if (type(self.input_weights) != list):
            mul.writeToFle()
            add.writeToFle()
        else:
            hadder.writeToFle()
            matmul.writeToFle()
            act = Activate_Vector(self.activation)
            act.writeToFle()
        
        """
        return complete VHDL definition of Gate
        """
        return f"""
        {VHDL_LIBRARIES}
        {VHDL_LIBRARY_DECLARATION}

        {self.getEntity()}

        architecture Behavioral of {self.name} is
        {matmul.getComponent() if (type(self.input_weights) == list) else mul.getComponent()}
        {hadder.getComponent() if (type(self.gate_biases) == list) else add.getComponent()}
        {sig.getComponent() if self.activation == 'sig' else tanh.getComponent()}
        {act.getComponent() if (type(self.input_weights) == list) else ""}

        -- temporary variables to store intermediate computations
        signal long_tmp   : output_type;
        signal scaled_down_tmp : output_type;
        signal short_tmp  : output_type;

        signal short_c    : output_type;
        signal input_c    : output_type;
        signal tmp_sum    : output_type;

        signal short_done : std_logic;
        signal input_done : std_logic;
        signal sum_done   : std_logic;
        signal sum_en     : std_logic;
        signal long_en    : std_logic;
        signal long_done  : std_logic;
        signal scale_done : std_logic;
        signal long_remember_done : std_logic;

        signal activate_done : std_logic;
        {"signal tmp_activate_done : std_logic_vector(0 to long_tmp'length-1);" if (type(self.input_weights) == list) else ""}
        ------------------------------------------

        begin
            {'-- initialise weights and biases if of array type\n'}
            {matmul.getInstance('clk', 'EN', 'input', 'input_weights', 'input_C', 'input_done')
              if (type(self.input_weights) == list) 
              else mul.getInstance('clk', 'EN', 'input', 'input_weights', 'input_c', 'input_done')}
            {matmul.getInstance('clk', 'EN', 'short', 'short_weights', 'short_c', 'short_done')
              if (type(self.input_weights) == list) 
              else mul.getInstance('clk', 'EN', 'short', 'short_weights', 'short_c', 'short_done')}
            
            Adder_enable: process(clk)
            begin
                if rising_edge(clk) then
                    if (short_done = '1' and input_done = '1') then
                        sum_en <= '1';
                    else
                        sum_en <= '0';
                    end if;
                end if;
            end process;
            
            {hadder.getInstance('clk', 'sum_en', 'input_c', 'short_c', 'tmp_sum', 'sum_done')
              if (type(self.input_weights) == list) 
              else add.getInstance('clk', 'sum_en', 'input_c', 'short_c', 'tmp_sum', 'sum_done')}
            
            long_update_enable: process(clk)
            begin
                if rising_edge(clk) then
                    if (sum_done = '1') then
                        long_en <= '1';
                    else
                        long_en <= '0';
                    end if;
                end if;
            end process;

            {hadder.getInstance('clk', 'long_en', 'tmp_sum', 'gate_biases', 'long_tmp', 'long_done')
              if (type(self.input_weights) == list) 
              else add.getInstance('clk', 'long_en', 'tmp_sum', 'gate_biases', 'long_tmp', 'long_done')}

        scale_down_long: process(clk)
        begin
            if rising_edge(clk) then
                if long_done = '1' then
                     {'scaled_down_tmp <= long_tmp/1000;' if (type(self.input_weights) != list) else 
                     "for i in 0 to long_tmp'length-1 loop\n\tfor j in 0 to long_tmp(i)'length-1 loop\n\tscaled_down_tmp(i)(j) <= long_tmp(i)(j)/1000;\n\tend loop;\nend loop;"}
                    scale_done <= '1';
                end if;
            end if;
        end process;

        {"activate : for i in 0 to long_tmp'length - 1 generate" if (type(self.input_weights) == list) else ""}
            {(sig.getInstance('clk', 'scale_done', 'scaled_down_tmp', 'output', 'activate_done') if self.activation == "sig" else tanh.getInstance('clk', 'scale_done', 'scaled_down_tmp' , 'output', 'activate_done')) if (type(self.input_weights) != list) else ""}
            {(act.getInstance('clk', 'scale_done', 'scaled_down_tmp(i)', 'output(i)', 'tmp_activate_done(i)')) if (type(self.input_weights) == list) else ""}
        {"end generate activate;" if (type(self.input_weights) == list) else ""}

        {'''process(clk)
        begin
            if tmp_activate_done(tmp_activate_done'length-1) = '1' then
                activate_done <= '1';
            end if;
        end process;''' if (type(self.input_weights) == list) else ""}

        process (clk)
        begin
        if rising_edge(clk) then
            if en = '1' then
                if activate_done = '1' then
                    done <= '1';
                end if;
            else
                done <= '0';
            end if;
        end if;
        end process;
        end architecture;
        """

class LSTM_Cell(Component):
    count = 0
    def __init__(self, forget_data, input_data, candidate_data, output_data):
        self.input_data = input_data
        self.candidate_data = candidate_data
        self.output_data = output_data
        self.forget_data = forget_data

    @property
    def name(self)->str:
        return f'lstm_cell'

    def getEntity(self) -> str:
        return f"""
        entity {self.name} is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                input         : in output_type;
                long          : in output_type;
                short         : in output_type;
                new_long      : out output_type;
                new_short     : out output_type;
                done          : out std_logic
            );
        end entity {self.name};
        """
    def getComponent(self)->str:
        return f"""
        component {self.name} is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                input         : in output_type;
                long          : in output_type;
                short         : in output_type;
                new_long      : out output_type;
                new_short     : out output_type;
                done          : out std_logic
            );
        end component;
        """

    def getInstance(self, clk, EN, input, long, short, new_long, new_short, done) -> str:
        self.count += 1
        return f"""
        {self.name}_inst_{self.count-1}: {self.name} port map(
            clk          => {clk},
            EN           => {EN},
            input        => {input},
            long         => {long},
            short        => {short},
            new_long     => {new_long},
            new_short    => {new_short},
            done         => {done}
        );
        """

    def toVHDL(self) -> str:
        forgetGate = Gate('forget_gate', self.forget_data["input_weights"], self.forget_data["gate_biases"], self.forget_data["short_weights"], 'sig')
        inputGate = Gate('input_gate', self.input_data["input_weights"], self.input_data["gate_biases"], self.input_data["short_weights"], 'tanh')
        candidateGate = Gate('candidate_gate', self.candidate_data["input_weights"], self.candidate_data["gate_biases"], self.candidate_data["short_weights"], 'sig')
        outputGate = Gate('output_gate', self.output_data["input_weights"], self.output_data["gate_biases"], self.output_data["short_weights"], 'sig')
        activate_vect = Activate_Vector('tanh')

        print(forgetGate.writeToFle())
        print(inputGate.writeToFle())
        print(candidateGate.writeToFle())
        print(outputGate.writeToFle())
        print(elmul.writeToFle())
        """
        return complete VHDL definition of Gate
        """
        return f"""
        {VHDL_LIBRARIES}
        {VHDL_LIBRARY_DECLARATION}

        {self.getEntity()}

        architecture Behavioral of {self.name} is
        {forgetGate.getComponent()}
        {inputGate.getComponent()}
        {candidateGate.getComponent()}
        {outputGate.getComponent()}
        {matmul.getComponent() if (type(self.input_data['input_weights']) == list) else mul.getComponent()}
        {hadder.getComponent() if (type(self.input_data['gate_biases']) == list) else add.getComponent()}
        {tanh.getComponent()}
        {elmul.getComponent() if type(self.input_data['input_weights']) else ""}
        {activate_vect.getComponent() if type(self.input_data['input_weights']) else ""}

        signal forget_gate_output     : output_type; -- long_remember percent
        signal forget_gate_done       : std_logic;

        signal tmp_new_long           : output_type;
        signal tmp_new_short          : output_type;
        signal new_long_memory        : output_type;
        signal new_short_memory       : output_type;

        signal input_gate_output      : output_type; -- potential memory
        signal input_gate_done        : std_logic;

        signal input_candidate_en     : std_logic;
        signal update_long_en         : std_logic;
        signal long_update_done       : std_logic;
        signal sum_update_en          : std_logic;
        signal long_tmp1_done         : std_logic;
        signal long_tmp2_done         : std_logic;

        signal long_tmp1              : output_type;
        signal long_tmp2              : output_type;

        signal candidate_gate_output  : output_type; -- potential remember percent
        signal candidate_gate_done    : std_logic;

        signal output_gate_output     : output_type; -- output percent
        signal output_gate_done       : std_logic;
        signal scaled_down_tmp        : output_type;
        signal scale_done             : std_logic;

        signal output_tmp             : output_type;
        signal tmp_active_done        : std_logic;
        signal short_scale_done       : std_logic;

        begin
        {forgetGate.getInstance('clk', 'EN', 'input', 'short', 'forget_gate_output', 'forget_gate_done')}
        {inputGate.getInstance('clk', 'EN', 'input', 'short', 'input_gate_output', 'input_gate_done')}
        {candidateGate.getInstance('clk', 'EN', 'input', 'short', 'candidate_gate_output', 'candidate_gate_done')}

        {elmul.getInstance('clk', 'forget_gate_done', 'long', 'forget_gate_output', 'long_tmp1', 'long_tmp1_done')
              if (type(self.input_data['input_weights']) == list) 
              else mul.getInstance('clk', 'forget_gate_done', 'long', 'forget_gate_output', 'long_tmp1', 'long_tmp1_done')}

        process(clk)
        begin
            if rising_edge(clk) then
                if (candidate_gate_done = '1' and input_gate_done = '1') then
                    input_candidate_en <= '1';
                else
                    input_candidate_en <= '0';
                end if;
            end if;
        end process;

        {elmul.getInstance('clk', 'input_candidate_en', 'candidate_gate_output', 'input_gate_output', 'long_tmp2', 'long_tmp2_done')
              if (type(self.input_data['input_weights']) == list)
              else mul.getInstance('clk', 'input_candidate_en', 'candidate_gate_output', 'input_gate_output', 'long_tmp2', 'long_tmp2_done')}

        update_long_memory : process(clk)
        begin
            if rising_edge(clk) then
                if (long_tmp1_done = '1' and long_tmp2_done = '1') then
                    sum_update_en <= '1';
                end if;
            end if;
        end process;

        {hadder.getInstance('clk', 'sum_update_en', 'long_tmp1', 'long_tmp2', 'new_long_memory', 'long_update_done')
              if (type(self.input_data['input_weights']) == list) 
              else add.getInstance('clk', 'sum_update_en', 'long_tmp1', 'long_tmp2', 'new_long_memory', 'long_update_done')}

        {outputGate.getInstance('clk', 'EN', 'input', 'short', 'output_gate_output', 'output_gate_done')}

        scale_down_long: process(clk)
        begin
            if rising_edge(clk) then
                if long_update_done = '1' then
                    {'scaled_down_tmp <= new_long_memory/1000;' if (type(self.input_data['input_weights']) != list) else 
                     "for i in 0 to new_long_memory'length-1 loop\n\tfor j in 0 to new_long_memory(i)'length-1 loop\n\tscaled_down_tmp(i)(j) <= new_long_memory(i)(j)/1000;\n\tend loop;\nend loop;"}
                    scale_done <= '1';
                end if;
            end if;
        end process;

        {"activate : for i in 0 to new_long_memory'length - 1 generate" if (type(self.input_data['input_weights']) == list) else ""}
            {tanh.getInstance('clk', 'scale_done', 'scaled_down_tmp', 'output_tmp', 'tmp_active_done') if type(self.input_data['input_weights']) != list else ""}
            {activate_vect.getInstance('clk', 'scale_done', 'scaled_down_tmp(i)', 'output_tmp(i)', 'tmp_active_done') if type(self.input_data['input_weights']) == list else ""}
        {"end generate activate;" if (type(self.input_data['input_weights']) == list) else ""}

        {elmul.getInstance('clk', 'tmp_active_done', 'output_tmp', 'output_gate_output', 'tmp_new_short', 'short_scale_done')
              if (type(self.input_data['input_weights']) == list)
              else mul.getInstance('clk', 'tmp_active_done', 'output_tmp', 'output_gate_output', 'tmp_new_short', 'short_scale_done')}

        process(clk)
        begin
            if rising_edge(clk) then
                if short_scale_done = '1' then
                    {'new_short <= tmp_new_short/1000;' if (type(self.input_data['input_weights']) != list)
                     else "for i in 0 to new_short'length-1 loop\n\t\tfor j in 0 to new_short(0)'length-1 loop\n\tnew_short(i)(j) <= tmp_new_short(i)(j)/1000;\t\nend loop;\nend loop;"}
                    new_long <= scaled_down_tmp;
                    done <= '1';
                end if;
            end if;
        end process;
        end Behavioral;

        """

class LSTM_Unit(Component):
    count = 0
    def __init__(self, forget_data, input_data, candidate_data, output_data, n_inputs, input_shape, weight_shape):
        self.weight_shape = weight_shape
        self.n_inputs = n_inputs
        self.input_shape = input_shape
        self.input_data = input_data
        self.candidate_data = candidate_data
        self.output_data = output_data
        self.forget_data = forget_data

    @property
    def name(self)->str:
        return f'lstm_unit_{self.count}'
    
    def getEntity(self) -> str:
        return f"""
        entity {self.name} is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                inputs        : in input_array;
                output        : out output_type;
                done          : out std_logic
            );
        end entity {self.name};
        """
    
    def getComponent(self) -> str:
        return f"""
        Component {self.name} is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                inputs        : in input_array;
                output        : out output_type;
                done          : out std_logic
            );
        end component;
        """
    
    def getInstance(self, clk, EN, inputs, output, done) -> str:
        return f"""
        {self.name}_inst: {self.name} port map(
            clk   => {clk},
            EN    => {EN},
            inputs=> {inputs}
            output=> {output}
            done  => {done}
        );
        """
    
    def toVHDL(self) -> str:
        lstm_cell = LSTM_Cell(self.forget_data, self.input_data, self.candidate_data, self.output_data)
        conf = Configuration(self.input_shape, self.weight_shape, self.n_inputs)
        print(conf.writeToFle())
        print(lstm_cell.writeToFle())
        arr = 0 if self.input_shape[0] == 1 and self.input_shape[1] == 1 else 1
        """
        return complete VHDL definition of Gate
        """
        return f"""
        {VHDL_LIBRARIES}
        {VHDL_LIBRARY_DECLARATION}

        {self.getEntity()}

        architecture Behavioral of {self.name} is
        {lstm_cell.getComponent()}

        signal unit1_done: std_logic;
        signal unit2_done: std_logic;
        signal unit3_done: std_logic;
        
        signal short : output_type := {'0' if arr != 1 else '(others => (others => 0))'};
        signal long  : output_type := {'0' if arr != 1 else '(others => (others => 0))'}; -- consider making it input of lstm_unit or instantiate

        signal short1: output_type;
        signal long1 : output_type;

        signal short2: output_type;
        signal long2 : output_type;

        signal short3: output_type;
        signal long3 : output_type;

        -- short4 is the output so is netted to the unit output
        signal long4 : output_type;

        begin
        {lstm_cell.getInstance('clk', 'EN', 'inputs(0)', 'long', 'short', 'long1', 'short1', 'unit1_done')}
        {lstm_cell.getInstance('clk', 'unit1_done', 'inputs(1)', 'long1', 'short1', 'long2', 'short2', 'unit2_done')}
        {lstm_cell.getInstance('clk', 'unit2_done', 'inputs(2)', 'long2', 'short2', 'long3', 'short3', 'unit3_done')}
        {lstm_cell.getInstance('clk', 'unit3_done', 'inputs(3)', 'long3', 'short3', 'long4', 'output', 'done')}

    end Behavioral;
        """


if __name__ == "__main__":
    # forgetGate = Gate('forget', 2, 1, 4, 'sig')
    # inputGate = Gate('input', 2, 1, 4, 'tanh')
    # candidateGate = Gate('candidate', 2, 1, 4, 'sig')
    # outputGate = Gate('output', 2, 1, 4, 'sig')
    
    # print(testGate.toVHDL())
    # print(forgetGate.writeToFle())
    # print(inputGate.writeToFle())
    # print(candidateGate.writeToFle())
    # print(outputGate.writeToFle())
    data = [{'input_weights': [[-1654, -486, -142, 1539], [1535, -2049, 253, -346], [1097, 892, -11, -9], [1181, 238, 1550, 935]], 'gate_biases': [0, 0, 0, 0], 'short_weights': [[-2247, -230, -1326, -66], [1615, -423, -1022, -1351], [-33, 46, -600, 2063], [495, 1572, -528, 227]]},
{'input_weights': [[-545, 273, 1106, -1404], [1063, -1128, -1974, -207], [-311, -482, 1543, 627], [1075, 998, -202, 1171]], 'gate_biases': [0, 0, 0, 0], 'short_weights': [[-868, 1021, 77, -346], [-203, -109, -1647, -986], [1098, -1345, -318, -744], [1053, -313, -669, 988]]},
{'input_weights': [[-766, 1392, -676, 116], [-433, 346, 1506, -2652], [181, 387, 544, 1434], [1748, -777, 1126, 1157]], 'gate_biases': [0, 0, 0, 0], 'short_weights': [[247, -582, -713, -1257], [1454, 81, 1163, -1622], [69, -234, 1634, -12], [383, -1670, 872, -969]]},
{'input_weights': [[109, 678, -347, -836], [35, 818, 160, 56], [2472, 299, 151, -1184], [1474, 857, 292, 883]], 'gate_biases': [0, 0, 0, 0], 'short_weights': [[434, 1395, -971, -234], [181, 563, 9, 1849], [179, 499, 27, 1168], [-1000, -160, -471, 89]]}]
    lSTM_Unit = LSTM_Unit(data[0], data[2], data[1], data[3], 4, [1, 4], [4, 4])
    print(lSTM_Unit.writeToFle())

