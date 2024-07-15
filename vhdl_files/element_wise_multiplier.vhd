
        
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
                mat1          : in output_type;
                mat2          : in output_type;
                mat12         : out output_type;
                done          : out std_logic
            );
            function vect_mul(signal vect1:output_row; signal vect2:output_row)
                return output_row is
                variable row: output_row;
                begin
                for i in 0 to vect2'length(1)-1 loop
                    row(i) := vect1(i) * vect2(i);
                end loop;
                return row;
            end vect_mul;
        end entity;
        
        architecture Behavioral of element_wise_multiplier is
        signal in1 : output_row;
        signal in2 : output_row;
        begin
            process (clk)
            variable tmp : const_int;
            variable tmp_out : output_type;
            begin
                if rising_edge(clk) then
                    if en = '1' then
                        for i in 0 to mat1'length-1 loop
                            in1 <= mat1(i);
                            in2 <= mat2(i);
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
        