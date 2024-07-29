
        
library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
-- use IEEE.fixed_pkg.all;

        
library work;       -- Default package name
use work.config.all;


        
        entity adder is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                input         : in const_int;
                bias          : in const_int;
                sum           : out const_int;
                done          : out std_logic
            );
        end entity adder;
        

        architecture Behavioral of adder is
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
        