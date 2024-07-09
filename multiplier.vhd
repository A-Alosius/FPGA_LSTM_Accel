
        
library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
-- use IEEE.fixed_pkg.all;

        
library work;       -- Default package name
use work.config.all;

        
        entity multiplier is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                num1, num2    : in const_int;
                prod          : out const_int;
                done          : out std_logic
            );
        end entity;
        
        architecture Behavioral of multiplier is
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
        