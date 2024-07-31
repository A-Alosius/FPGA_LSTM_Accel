
        
library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
-- use IEEE.fixed_pkg.all;

        
library work;       -- Default package name
use work.config.all;

        
        entity bin2num is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                bits   : in std_logic_vector(9 downto 0);
                number : out const_int;
                done   : out std_logic
            );
        end bin2num;
        

        architecture Behavioral of bin2num is
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
                        num := (ints(9)*1) + (ints(8)*2) + (ints(7)*4) + (ints(6)*8) + (ints(5)*16) + (ints(4)*32) + (ints(3)*64) + (ints(2)*128) + (ints(1)*256) + (ints(0)*512);
                        number <= num;
                        done <= '1';
                    else
                        done <= '0';
                    end if;
                end if;
            end process;
        end behavioral;
        