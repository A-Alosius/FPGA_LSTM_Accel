
        
library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
-- use IEEE.fixed_pkg.all;

        
library work;       -- Default package name
use work.config.all;


        
        entity lstm_cell is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                input         : in input_type;
                long          : in input_type;
                short         : in input_type;
                new_long      : out output_type;
                new_short     : out output_type;
                done          : out std_logic
            );
        end entity lstm_cell;
        

        architecture Behavioral of lstm_cell is
        
        component forget_gate is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                input         : in input_type;
                short         : in input_type;
                output        : out output_type;
                done          : out std_logic
            );
        end component;
        
        
        component input_gate is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                input         : in input_type;
                short         : in input_type;
                output        : out output_type;
                done          : out std_logic
            );
        end component;
        
        
        component candidate_gate is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                input         : in input_type;
                short         : in input_type;
                output        : out output_type;
                done          : out std_logic
            );
        end component;
        
        
        component output_gate is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                input         : in input_type;
                short         : in input_type;
                output        : out output_type;
                done          : out std_logic
            );
        end component;
        
        
        component matrix_multiplier is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                mat1          : in input_type;
                mat2          : in weight_type;
                mat12         : out output_type;
                done          : out std_logic
            );
        end component;
        
        
        component higher_adder is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                input_vector  : in input_row;
                bias          : in output_type;
                sum           : out output_type;
                done          : out std_logic
            );
        end component;
        
        
        component tanh_activation is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                num    : in integer;
                result : out integer;
                done   : out std_logic
            );
        end component;
        
        
        component element_wise_multiplier is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                mat1          : in input_type;
                mat2          : in input_type;
                mat12         : out input_type;
                done          : out std_logic
            );
        end component;
        

        signal forget_gate_output     : output_type; -- long_remember percent
        signal forget_gate_done       : std_logic;

        signal tmp_new_long           : output_type;
        signal tmp_new_short          : output_type;
        signal new_long_memory        : output_type;
        signal new_short_memory       : output_type;

        signal input_gate_output      : output_type; -- potential memory
        signal input_gate_done        : std_logic;

        signal input_candidate_en     : std_logic;
        signal update_long_en         : std_logic;
        signal long_update_done       : std_logic;
        signal sum_update_en          : std_logic;
        signal long_tmp1_done        : std_logic;
        signal long_tmp2_done        : std_logic;

        signal long_tmp1              : output_type;
        signal long_tmp2              : output_type;

        signal candidate_gate_output  : output_type; -- potential remember percent
        signal candidate_gate_done    : std_logic;

        signal output_gate_output     : output_type; -- output percent
        signal output_gate_done       : std_logic;
        signal scaled_down_tmp        : output_type;
        signal scale_done             : std_logic;

        signal output_tmp             : output_type;
        signal tmp_active_done        : std_logic;
        signal short_scale_done       : std_logic;

        begin
        
        forget_gate_inst: forget_gate port map(
            clk          => clk,
            EN           => EN,
            input        => input,
            short        => short,
            output       => forget_gate_output,
            done         => forget_gate_done
        );
        
        
        input_gate_inst: input_gate port map(
            clk          => clk,
            EN           => EN,
            input        => input,
            short        => short,
            output       => input_gate_output,
            done         => input_gate_done
        );
        
        
        candidate_gate_inst: candidate_gate port map(
            clk          => clk,
            EN           => EN,
            input        => input,
            short        => short,
            output       => candidate_gate_output,
            done         => candidate_gate_done
        );
        

        
        element_wise_multiplier_inst_0: element_wise_multiplier port map(
            clk   => clk,
            EN    => forget_gate_done,
            mat1  => long,
            mat2  => forget_gate_output,
            mat12 => long_tmp1,
            done  => long_tmp1_done
        );
        

        process(clk)
        begin
            if rising_edge(clk) then
                if (candidate_gate_done = '1' and input_gate_done = '1') then
                    input_candidate_en <= '1';
                else
                    input_candidate_en <= '0';
                end if;
            end if;
        end process;

        
        element_wise_multiplier_inst_1: element_wise_multiplier port map(
            clk   => clk,
            EN    => input_candidate_en,
            mat1  => candidate_gate_output,
            mat2  => input_gate_output,
            mat12 => long_tmp2,
            done  => long_tmp2_done
        );
        

        update_long_memory : process(clk)
        begin
            if rising_edge(clk) then
                if (long_tmp1_done = '1' and long_tmp2_done = '1') then
                    sum_update_en <= '1';
                end if;
            end if;
        end process;

        
        higher_adder_inst_8: higher_adder port map(
            clk          => clk,
            EN           => sum_update_en,
            input_vector => long_tmp1,
            bias         => long_tmp2,
            sum          => new_long_memory,
            done         => long_update_done
        );
        

        
        output_gate_inst: output_gate port map(
            clk          => clk,
            EN           => EN,
            input        => input,
            short        => short,
            output       => output_gate_output,
            done         => output_gate_done
        );
        

        scale_down_long: process(clk)
        begin
            if rising_edge(clk) then
                if long_update_done = '1' then
                    new_long <= new_long_memory/1000;
                    for i in 0 to new_long_memory'length loop
	new_long_memory(i) <= new_long_memory(i)/1000;
end loop;
                    scale_done <= '1';
                end if;
            end if;
        end process;

        activate : for i in 0 to long_tmp'length - 1 generate
            
        tanh_activation_inst_1: tanh_activation port map(
            clk    => clk,
            EN     => scale_done,
            num    => scaled_down_tmp(i),
            result => output_tmp(i),
            done   => tmp_active_done
        );
        
        end generate activate;

        
        element_wise_multiplier_inst_2: element_wise_multiplier port map(
            clk   => clk,
            EN    => tmp_active_done,
            mat1  => output_tmp,
            mat2  => output_gate_output,
            mat12 => tmp_new_short,
            done  => short_scale_done
        );
        

        process(clk)
        begin
            if rising_edge(clk) then
                if short_scale_done = '1' then
                    for i in 0 to new_short'length loop
	new_short(i) <= new_short(i)/1000;
end loop;
                    done <= '1';
                end if;
            end if;
        end process;
        end Behavioral;

        