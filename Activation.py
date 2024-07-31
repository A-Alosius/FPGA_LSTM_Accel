from Constants import VHDL_LIBRARIES, VHDL_LIBRARY_DECLARATION
from Component import Component
import math

# input_range = [-1, 5]
# precision = 0.01
# dp = 3

class Activation(Component):
    """Base for all activation functions"""
    count = 0

    def __init__(self, input_range, accuracy, dp):
        self.input_range = input_range
        self.accuracy = accuracy
        self.dp = dp

    @property
    def name(self):
        return 'null_activation'
    
    def getEntity(self):
        return f"""
        entity {self.name} is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                num    : in integer;
                result : out integer;
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
                num    : in integer;
                result : out integer;
                done   : out std_logic
            );
        end component;
        """
    
    def getInstance(self, clk, EN, num, result, done):
        self.count += 1
        return f"""
        {self.name}_inst_{self.count-1}: {self.name} port map(
            clk    => {clk},
            EN     => {EN},
            num    => {num},
            result => {result},
            done   => {done}
        );
        """
    
class Sigmoid(Activation):
    """Sigmoid activation function: sig(x) using ROM"""

    @property
    def name(self):
        return 'sigmoid'
    
    def values(self):
        sig = []
        i = self.input_range[0]
        while i < self.input_range[1]:
            sig.append(int((1/(1 + math.exp(-i)))*10**self.dp))
            i += self.accuracy
        return sig

    
    def toVHDL(self):
        sig = self.values()
        rom = "("
        k = 0

        for i in sig:
            rom += str(i)
            if k == len(sig)-1:
                break
            rom += ','
            k += 1
        rom += ")"

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

            process(clk)
            variable sigm : int_array := {rom};
            begin

                if rising_edge(clk) then
                    if EN = '1' then
                        if num > {int((self.input_range[0]/self.accuracy)*(self.accuracy*10**self.dp))} and num < {(len(sig)-1)*int(self.accuracy*10**self.dp)} then
                            result <= sigm(({int((0-self.input_range[0])/self.accuracy)}) + num/{int(self.accuracy*10**self.dp)}); -- take note of precision if 0.1 leave as is if 0.01 divide by 1
                            done <= '1';
                        else
                            result <= 0;
                            done <= '1';
                        end if;
                    else
                        done <= '0';
                    end if;
                end if;
            end process;
        end behavioral;
        """
    
class Tanh(Activation):
    """Tanh activation function: tanh(x) using ROM"""

    @property
    def name(self):
        return 'tanh_activation'
    
    def values(self):
        tanh = []
        i = self.input_range[0]
        while i < self.input_range[1]:
            tanh.append(int(math.tanh(i)*10**self.dp))
            i += self.accuracy
        return tanh

    
    def toVHDL(self):
        tanh = self.values()
        rom = "("
        k = 0

        for i in tanh:
            rom += str(i)
            if k == len(tanh)-1:
                break
            rom += ','
            k += 1
        rom += ")"

        return f"""
        {VHDL_LIBRARIES}
        package dtypes is
            type int_array is array (0 to {len(tanh)-1}) of integer;
        end package;

        {VHDL_LIBRARIES}
        {VHDL_LIBRARY_DECLARATION}
        use work.dtypes.all;
        {self.getEntity()}

        architecture Behavioral of {self.name} is
        begin

            process(clk)
            variable tanh : int_array := {rom};
            begin

                if rising_edge(clk) then
                    if EN = '1' then
                        if num > {int((self.input_range[0]/self.accuracy)*(self.accuracy*10**self.dp))} and num < {(len(tanh)-1)*int(self.accuracy*10**self.dp)} then
                            result <= tanh(({int((0-self.input_range[0])/self.accuracy)}) + num/{int(self.accuracy*10**self.dp)}); -- take note of precision if 0.1 leave as is if 0.01 divide by 1
                            done <= '1';
                        else
                            result <= 0;
                            done <= '1';
                        end if;
                    else
                        done <= '0';
                    end if;
                end if;
            end process;
        end behavioral;
        """
    
class Activate_Vector(Component):
    count = 0
    def __init__(self, activation, input_range, accuracy, dp) -> None:
        self.input_range = input_range
        self.accuracy = accuracy
        self.dp = dp
        self.activation = activation
    
    @property
    def name(self):
        return f"vector_activation_{self.activation}"
    
    def getEntity(self):
        return f"""
        entity {self.name} is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                vector : in output_row;
                result : out output_row;
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
                vector : in output_row;
                result : out output_row;
                done   : out std_logic
            );
        end component;
        """
    
    def getInstance(self, clk, EN, vector, result, done):
        self.count += 1
        return f"""
        {self.name}_inst_{self.count-1}: {self.name} port map(
            clk    => {clk},
            EN     => {EN},
            vector => {vector},
            result => {result},
            done   => {done}
        );
        """
    
    def toVHDL(self):
        if self.activation == 'sig':
            act = Sigmoid(self.input_range, self.accuracy, self.dp)
        else:
            act = Tanh(self.input_range, self.accuracy, self.dp)

        return f"""
        {VHDL_LIBRARIES}

        {VHDL_LIBRARIES}
        {VHDL_LIBRARY_DECLARATION}
        use work.dtypes.all;
        {self.getEntity()}

        architecture Behavioral of {self.name} is
        {act.getComponent()}
        
        signal tmp_output : output_row;
        signal tmp_done : std_logic_vector(0 to vector'length-1);
        begin
            vector_activate: for i in 0 to vector'length-1 generate
                {act.getInstance('clk', 'en', 'vector(i)', 'tmp_output(i)', 'tmp_done(i)')}
            end generate vector_activate;
            process(clk)
            begin
                if (tmp_done(tmp_done'length-1) = '1') then
                    done <= '1';
                    result <= tmp_output;
                end if;
            end process;
        end behavioral;
        """
if __name__ == "__main__":
    testActivation = Tanh([-1, 10], 0.01, 3)
    # a = testActivation.values(input_range, precision)
    # sig = Sigmoid().values(input_range, precision)
    # print(len(a))
    # print(testActivation[44])
    print(testActivation.writeToFle())
    # print(testActivation1.writeToFle())