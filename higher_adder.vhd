
        
library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
-- use IEEE.fixed_pkg.all;

        
library work;       -- Default package name
use work.config.all;


        
        entity higher_adder is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                input_vector  : in output_type;
                bias          : in output_type;
                sum           : out output_type;
                done          : out std_logic
            );
        end entity higher_adder;
        

        architecture Behavioral of higher_adder is
        begin
            process(clk)
                variable tmp_sum : output_type;
                variable tmp_arr : output_type;
                begin
                    if rising_edge(clk) then
                       -- if (en = '1') then
                         --   tmp_arr := input_vector;
                        --end if;
                        for i in 0 to (input_vector'length-1) loop
                            for j in 0 to input_vector(i)'length-1 loop
                                tmp_sum(i)(j) := input_vector(i)(j) + bias(i)(j);
                            end loop;
                        end loop;
                        sum <= tmp_sum;
                        done <= '1';
                    end if;
                end process;
        end architecture;
        