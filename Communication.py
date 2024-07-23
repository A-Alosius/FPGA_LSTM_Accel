from Constants import VHDL_LIBRARIES, VHDL_LIBRARY_DECLARATION
from Component import Component
from Gate import LSTM_Unit
from Num2Bin import Num2Bin
import math

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
        return 'Communication_Modeule'
        
    def getEntity(self):
        return f"""
        entity {self.name} is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                rst    : in std_logic;
                ctrl   : in std_logic_vector(1 downto 0);
                inbits : in std_logic_vector({self.nbits} to 0);
                outbits: in std_logic_vector({self.nbits} to 0);
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
                inbits : in std_logic_vector({self.nbits} to 0);
                outbits: in std_logic_vector({self.nbits} to 0);
                );
        end component;
        """
    
    def getInstance(self, clk, EN, rst, ctrl, inbits, outbits):
        self.count += 1
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
        num2bin   = Num2Bin()
        return f"""
        {VHDL_LIBRARIES}
        -- package dtypes is
            -- type int_array is array (0 to {len(sig)-1}) of integer;
        -- end package;

        {VHDL_LIBRARIES}
        {VHDL_LIBRARY_DECLARATION}
        use work.dtypes.all;
        {self.getEntity()}

        architecture Behavioral of {self.name} is
        begin

        end behavioral;
        """
    