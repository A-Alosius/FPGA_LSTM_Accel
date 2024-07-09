
        
library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
-- use IEEE.fixed_pkg.all;

        
library work;       -- Default package name
use work.config.all;

        
        entity element_wise_multiplier is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                mat1          : in input_type;
                mat2          : in input_type;
                mat12         : out input_type;
                done          : out std_logic
            );
            function vect_mul(signal vect1:input_row; signal vect2:input_row)
                return input_row is
                variable row: input_row;
                begin
                for i in 0 to vect2'length(1)-1 loop
                    row(i) := vect1(i) * vect2(i);
                end loop;
                return row;
            end vect_mul;
        end entity;
        
        architecture Behavioral of element_wise_multiplier is
        begin
            process (clk)
            variable tmp : const_int;
            variable tmp_out : input_type;
            begin
                if rising_edge(clk) then
                    if en = '1' then
                        for i in 0 to mat1'length-1 loop
                            tmp_out(i)(j) := vect_mul(mat1(i), mat2(j));
                        end loop;
                        mat12 <= tmp_out;
                        done <= '1';
                    else
                        done <= '0';
                    end if;
                end if;
            end process;
        end architecture;
        