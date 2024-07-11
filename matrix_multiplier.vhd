
        
library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
-- use IEEE.fixed_pkg.all;

        
library work;       -- Default package name
use work.config.all;

        
        entity matrix_multiplier is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                mat1          : in output_type;
                mat2          : in weight_type;
                mat12         : out output_type;
                done          : out std_logic
            );
            function vect_mul(signal vect1:output_row; signal vect2:weight_row)
                return const_int is
                variable sum: const_int := 0;
                begin
                for i in 0 to vect2'length(1)-1 loop
                    sum := sum + (vect1(i) * vect2(i));
                end loop;
                return sum;
            end vect_mul;
        end entity;
        
        architecture Behavioral of matrix_multiplier is
        begin
        signal in1 : output_row;
        signal in2 : weight_row;
            process (clk)
            variable tmp_out : output_type;
            begin
                if rising_edge(clk) then
                    if en = '1' then
                        for i in 0 to mat1'length-1 loop
                            in1 <= mat1(i);
                            for j in 0 to mat2'length-1 loop
                                in2 <= mat2(j);
                                tmp_out(i) := vect_mul(in1, in2);
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
        