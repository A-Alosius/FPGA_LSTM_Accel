from Constants import VHDL_LIBRARIES, VHDL_LIBRARY_DECLARATION
from Component import Component

# The adder and multiply classes are adapted from Akotey Ian's ANN FPGA Acceleration : https://github.com/ianakotey/FPGA_Accelerator/blob/master/Generator/

class Adder(Component):
    count = 0

    @property
    def name(self)->str:
        return f'adder'
    
    def getEntity(self) -> str:
        return f"""
        entity {self.name} is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                input         : in const_int;
                bias          : in const_int;
                sum           : out const_int;
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
                input         : in const_int;
                bias          : in const_int;
                sum           : out const_int;
                done          : out std_logic
            );
        end component;
        """
    
    def getInstance(self, clk, EN, input, bias, sum, done) -> str:
        self.count += 1
        return f"""
        {self.name}_inst_{self.count-1} : {self.name} port map(
            clk          => {clk},
            EN           => {EN},
            input        => {input},
            bias         => {bias},
            sum          => {sum},
            done         => {done}
        );
        """
    
    def toVHDL(self) -> str:
        """
        return complete VHDL definition of Adder
        """
        return f"""
        {VHDL_LIBRARIES}
        {VHDL_LIBRARY_DECLARATION}

        {self.getEntity()}

        architecture Behavioral of {self.name} is
        begin
            process(clk)
                variable tmp_sum : const_int := 0;
                begin
                    if rising_edge(clk) then
                        if (en = '1') then 
                            sum <= input + bias;
                            done <= '1';
                        end if;
                    end if;
                end process;
        end architecture;
        """

class HigherBiasAdder(Component):
    count = 0

    @property
    def name(self)->str:
        return f'higher_adder'
    
    def getEntity(self) -> str:
        return f"""
        entity {self.name} is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                input         : in output_type;
                bias          : in output_type;
                sum           : out output_type;
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
                bias          : in output_type;
                sum           : out output_type;
                done          : out std_logic
            );
        end component;
        """
    
    def getInstance(self, clk, EN, input, bias, sum, done) -> str:
        self.count += 1
        return f"""
        {self.name}_inst_{self.count-1}: {self.name} port map(
            clk          => {clk},
            EN           => {EN},
            input       => {input},
            bias         => {bias},
            sum          => {sum},
            done         => {done}
        );
        """
    
    def toVHDL(self) -> str:
        """
        return complete VHDL definition of Adder
        """
        return f"""
        {VHDL_LIBRARIES}
        {VHDL_LIBRARY_DECLARATION}

        {self.getEntity()}

        architecture Behavioral of {self.name} is
        begin
            process(clk)
                variable tmp_sum : output_type;
                variable mat1    : output_type;
                variable mat2    : output_type;
                begin
                mat1 := input;
                mat2 := bias;
                    if rising_edge(clk) then
                        if en = '1' then
                            for i in 0 to (mat1'length-1) loop
                                for j in 0 to mat1(i)'length-1 loop
                                    tmp_sum(i)(j) := input(i)(j) + bias(i)(j);
                                end loop;
                            end loop;
                            sum <= tmp_sum;
                            done <= '1';
                        end if;
                    end if;
                end process;
        end architecture;
        """

# generate vhdl code for together multiplication
class Multiplier(Component):
    count = 0
    def __init__(self)->None:
        pass

    @property
    def name(self)->str:
        return 'multiplier'

    def getEntity(self)->str:
        return f"""
        entity {self.name} is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                num1, num2    : in const_int;
                prod          : out const_int;
                done          : out std_logic
            );
        end entity;
        """
    
    def getComponent(self) -> str:
        return f"""
        component {self.name} is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                num1, num2    : in const_int;
                prod          : out const_int;
                done          : out std_logic
            );
        end component;
        """
    
    def getInstance(self, clk, EN, num1, num2, prod, done) -> str:
        self.count += 1
        return f"""
        {self.name}_inst_{self.count-1}: {self.name} port map(
            clk   => {clk},
            EN    => {EN},
            num1  => {num1},
            num2  => {num2},
            prod  => {prod},
            done  => {done}
        );
        """
    
    def toVHDL(self) -> str:
        return f"""
        {VHDL_LIBRARIES}
        {VHDL_LIBRARY_DECLARATION}
        {self.getEntity()}
        architecture Behavioral of {self.name} is
        begin
            sum_process : process (clk)
            variable tmp : const_int := 0;
            begin
                if rising_edge(clk) then
                    if EN = '1' then
                        tmp := num1 * num2;
                        prod <= tmp;
                        done <= '1';
                    else
                        done <= '0';
                    end if;
                end if;
            end process;
        end architecture;
        """

class MatrixMultiplier(Component):
    count = 0
    def __init__(self)->None:
        pass

    @property
    def name(self)->str:
        return 'matrix_multiplier'

    def getEntity(self)->str:
        return f"""
        entity {self.name} is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                mat1          : in output_type;
                mat2          : in weight_type;
                mat12         : out output_type;
                done          : out std_logic
            );
            function vect_mul(vect1:output_row; vect2:weight_row)
                return const_int is
                variable sum: const_int := 0;
                begin
                for i in 0 to vect2'length(1)-1 loop
                    sum := sum + (vect1(i) * vect2(i));
                end loop;
                return sum;
            end vect_mul;
        end entity;
        """
    
    def getComponent(self) -> str:
        return f"""
        component {self.name} is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                mat1          : in output_type;
                mat2          : in weight_type;
                mat12         : out output_type;
                done          : out std_logic
            );
        end component;
        """
    
    def getInstance(self, clk, EN, mat1, mat2, mat12, done) -> str:
        self.count += 1
        return f"""
        {self.name}_inst_{self.count-1}: {self.name} port map(
            clk   => {clk},
            EN    => {EN},
            mat1  => {mat1},
            mat2  => {mat2},
            mat12 => {mat12},
            done  => {done}
        );
        """
    
    def toVHDL(self) -> str:
        return f"""
        {VHDL_LIBRARIES}
        {VHDL_LIBRARY_DECLARATION}
        {self.getEntity()}
        architecture Behavioral of {self.name} is
        begin
            process (clk)
            variable in1 : output_row;
            variable in2 : weight_row;
            variable tmp_out : output_type;
            begin
                if rising_edge(clk) then
                    if en = '1' then
                        for i in 0 to mat1'length-1 loop
                            in1 := mat1(i);
                            for j in 0 to mat2'length-1 loop
                                in2 := mat2(j);
                                tmp_out(i)(j) := vect_mul(in1, in2);
                            end loop;
                        end loop;
                        mat12 <= tmp_out;
                        done <= '1';
                    else
                        done <= '0';
                    end if;
                end if;
            end process;
        end architecture;
        """

class ElementWiseMultiplier(Component):
    count = 0
    def __init__(self)->None:
        pass

    @property
    def name(self)->str:
        return 'element_wise_multiplier'

    def getEntity(self)->str:
        return f"""
        entity {self.name} is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                mat1          : in output_type;
                mat2          : in output_type;
                mat12         : out output_type;
                done          : out std_logic
            );
            function vect_mul(vect1:output_row; vect2:output_row)
                return output_row is
                variable row: output_row;
                begin
                for i in 0 to vect2'length(1)-1 loop
                    row(i) := vect1(i) * vect2(i);
                end loop;
                return row;
            end vect_mul;
        end entity;
        """
    
    def getComponent(self) -> str:
        return f"""
        component {self.name} is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                mat1          : in output_type;
                mat2          : in output_type;
                mat12         : out output_type;
                done          : out std_logic
            );
        end component;
        """
    
    def getInstance(self, clk, EN, mat1, mat2, mat12, done) -> str:
        self.count += 1
        return f"""
        {self.name}_inst_{self.count-1}: {self.name} port map(
            clk   => {clk},
            EN    => {EN},
            mat1  => {mat1},
            mat2  => {mat2},
            mat12 => {mat12},
            done  => {done}
        );
        """
    
    def toVHDL(self) -> str:
        return f"""
        {VHDL_LIBRARIES}
        {VHDL_LIBRARY_DECLARATION}
        {self.getEntity()}
        architecture Behavioral of {self.name} is
        begin
            process (clk)
            variable in1 : output_row;
            variable in2 : output_row;
            variable tmp_out : output_type;
            begin
                if rising_edge(clk) then
                    if en = '1' then
                        for i in 0 to mat1'length-1 loop
                            in1 := mat1(i);
                            in2 := mat2(i);
                            tmp_out(i) := vect_mul(in1, in2);
                        end loop;
                        mat12 <= tmp_out;
                        done <= '1';
                    else
                        done <= '0';
                    end if;
                end if;
            end process;
        end architecture;
        """
    
if __name__ == "__main__":
    # test multiplier
    testMultiplier = MatrixMultiplier()
    testMultiplier1 = Multiplier()
    testMultiplier2 = Adder()
    testMultiplier3 = HigherBiasAdder()
    # print(testMultiplier.getEntity())
    # print(testMultiplier.getInstance("clk", "EN", "mat1", "mat2", "mat12", "done"))
    # print(testMultiplier.getInstance("clk", "EN", "mat1", "mat2", "mat12", "done"))
    print(testMultiplier.writeToFle())
    print(testMultiplier1.writeToFle())
    print(testMultiplier2.writeToFle())
    print(testMultiplier3.writeToFle())
    # testMultiplier.writeToFle()