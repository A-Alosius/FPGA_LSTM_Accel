from Constants import VHDL_LIBRARIES, VHDL_LIBRARY_DECLARATION
from Component import Component

class Num2Bin(Component):
    """Converts integers to bits"""
    def __init__(self, nbits):
        self.nbits = nbits

    @property
    def name(self):
        return 'num2bin'
    
    def getEntity(self):
        return f"""
        entity {self.name} is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                number : in const_int;
                bits   : out std_logic_vector({self.nbits} downto 0);
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
                number : in const_int;
                bits   : out std_logic_vector({self.nbits} downto 0);
                done   : out std_logic
            );
        end component;
        """
    
    def getInstance(self, clk, EN, num, bits, done):
        return f"""
        {self.name}_inst: {self.name} port map(
            clk    => {clk},
            EN     => {EN},
            number => {num},
            bits   => {bits},
            done   => {done}
        );
        """
    
    def toVHDL(self) -> str:
        return f"""
        {VHDL_LIBRARIES}
        {VHDL_LIBRARY_DECLARATION}
        {self.getEntity()}

        architecture Behavioral of {self.name} is
        begin
            process(clk)
                variable tmp_bits : std_logic_vector({self.nbits} downto 0);
                variable num : const_int := number;
            begin
      	 
                if rising_edge(clk) then
                    if en = '1' then
                        num  := number;
                        for i in 0 to bits'length-1 loop
                            -- check the parity of current value of num and assign 1 is odd and zero if even
                            case num mod 2 is 
                            when 1 => 
                                    tmp_bits(i) := '1';
                            when 0 => 
                                    tmp_bits(i) := '0';
                            when others => 
                                    tmp_bits(i) := '0';  -- Handle unexpected values (optional)
                            end case;
                            -- divide num until we get to zero
                            num := num / 2; 
                        end loop;
                        bits <= tmp_bits;
                        done <= '1';
                    end if;
                end if;
            end process;
        end behavioral;
        """
    
class Bin2Num(Component):
    """Converts integers to bits"""
    def __init__(self, nbits):
        self.nbits = nbits

    @property
    def name(self):
        return 'bin2num'
    
    def getEntity(self):
        return f"""
        entity {self.name} is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                bits   : in std_logic_vector({self.nbits} downto 0);
                number : out const_int;
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
                bits   : in std_logic_vector({self.nbits} downto 0);
                number : out const_int;
                done   : out std_logic
            );
        end component;
        """
    
    def getInstance(self, clk, EN, num, bits, done):
        return f"""
        {self.name}_inst: {self.name} port map(
            clk    => {clk},
            EN     => {EN},
            bits   => {bits},
            number => {num},
            done   => {done}
        );
        """
    
    def computation(self):
        compute_string = ''
        for i in range(self.nbits):
            if i == self.nbits-1:
                compute_string += f'(ints({self.nbits-i-1})*{2**i})'
                return compute_string
            compute_string += f'(ints({self.nbits-i-1})*{2**i}) + '
    
    def toVHDL(self) -> str:
        return f"""
        {VHDL_LIBRARIES}
        {VHDL_LIBRARY_DECLARATION}
        {self.getEntity()}

        architecture Behavioral of {self.name} is
            signal ints : bin_int_array;
            begin
                process (clk)
                variable num : INTEGER := 0;
                begin
                
                if rising_Edge(clk) then
                    if (en = '1') then
                        for i in 0 to ints'length-1 loop
                            if bits(i) = '1' then
                                ints((ints'length-1)-i) <= 1;
                            else
                                ints((ints'length-1)-i) <= 0;
                            end if;
                        end loop;
                        
                        -- use loop to generatae this as one operation note the descending order of indexes
                        num := {self.computation()};
                        number <= num;
                        done <= '1';
                    else
                        done <= '0';
                    end if;
                end if;
            end process;
        end behavioral;
        """