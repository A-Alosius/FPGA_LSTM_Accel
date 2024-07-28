
        
library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
-- use IEEE.fixed_pkg.all;


        
library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
-- use IEEE.fixed_pkg.all;

        
library work;       -- Default package name
use work.config.all;

        use work.dtypes.all;
        
        entity vector_activation_tanh is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                vector : in output_row;
                result : out output_row;
                done   : out std_logic
            );
        end vector_activation_tanh;
        

        architecture Behavioral of vector_activation_tanh is
        
        component tanh_activation is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                num    : in integer;
                result : out integer;
                done   : out std_logic
            );
        end component;
        
        
        signal tmp_output : output_row;
        signal tmp_done : std_logic_vector(0 to vector'length-1);
        begin
            vector_activate: for i in 0 to vector'length-1 generate
                
        tanh_activation_inst_0: tanh_activation port map(
            clk    => clk,
            EN     => en,
            num    => vector(i),
            result => tmp_output(i),
            done   => tmp_done(i)
        );
        
            end generate vector_activate;
            process(clk)
            begin
                if (tmp_done(tmp_done'length-1) = '1') then
                    done <= '1';
                    result <= tmp_output;
                end if;
            end process;
        end behavioral;
        