
        
library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
-- use IEEE.fixed_pkg.all;

        
library work;       -- Default package name
use work.config.all;

        
        entity num2bin is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                number : in const_int;
                bits   : out std_logic_vector(9 downto 0);
                done   : out std_logic
            );
        end num2bin;
        

        architecture Behavioral of num2bin is
        begin
            process(clk)
                variable tmp_bits : std_logic_vector(9 downto 0);
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
        