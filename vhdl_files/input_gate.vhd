
        
library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
-- use IEEE.fixed_pkg.all;

        
library work;       -- Default package name
use work.config.all;


        
        entity input_gate is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                input         : in output_type;
                short         : in output_type;
                output        : out output_type;
                done          : out std_logic
            );

            -- declare and instantiate weight and biases for each gate here
            signal input_weights : weight_type;
            signal gate_biases   : output_type;
            signal short_weights : weight_type;
        end entity input_gate;
        

        architecture Behavioral of input_gate is
        
        component matrix_multiplier is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                mat1          : in output_type;
                mat2          : in weight_type;
                mat12         : out output_type;
                done          : out std_logic
            );
        end component;
        
        
        component higher_adder is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                input         : in output_type;
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
        
        
        component vector_activation_tanh is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                vector : in output_row;
                result : out output_row;
                done   : out std_logic
            );
        end component;
        

        -- temporary variables to store intermediate computations
        signal long_tmp   : output_type;
        signal scaled_down_tmp : output_type;
        signal short_tmp  : output_type;

        signal short_c    : output_type;
        signal input_c    : output_type;
        signal tmp_sum    : output_type;

        signal short_done : std_logic;
        signal input_done : std_logic;
        signal sum_done   : std_logic;
        signal sum_en     : std_logic;
        signal long_en    : std_logic;
        signal long_done  : std_logic;
        signal scale_done : std_logic;
        signal long_remember_done : std_logic;

        signal activate_done : std_logic;
        signal tmp_activate_done : std_logic_vector(0 to long_tmp'length-1);
        ------------------------------------------

        begin
            -- initialise weights and biases if of array type

            input_weights(0) <= (-766, 1392, -676, 116);
			input_weights(1) <= (-433, 346, 1506, -2652);
			input_weights(2) <= (181, 387, 544, 1434);
			input_weights(3) <= (1748, -777, 1126, 1157);
			
            short_weights(0) <= (247, -582, -713, -1257);
			short_weights(1) <= (1454, 81, 1163, -1622);
			short_weights(2) <= (69, -234, 1634, -12);
			short_weights(3) <= (383, -1670, 872, -969);
			
            gate_biases(0) <= (0, 0, 0, 0);
            
            
        matrix_multiplier_inst_2: matrix_multiplier port map(
            clk   => clk,
            EN    => EN,
            mat1  => input,
            mat2  => input_weights,
            mat12 => input_C,
            done  => input_done
        );
        
            
        matrix_multiplier_inst_3: matrix_multiplier port map(
            clk   => clk,
            EN    => EN,
            mat1  => short,
            mat2  => short_weights,
            mat12 => short_c,
            done  => short_done
        );
        
            
            Adder_enable: process(clk)
            begin
                if rising_edge(clk) then
                    if (short_done = '1' and input_done = '1') then
                        sum_en <= '1';
                    else
                        sum_en <= '0';
                    end if;
                end if;
            end process;
            
            
        higher_adder_inst_2: higher_adder port map(
            clk          => clk,
            EN           => sum_en,
            input       => input_c,
            bias         => short_c,
            sum          => tmp_sum,
            done         => sum_done
        );
        
            
            long_update_enable: process(clk)
            begin
                if rising_edge(clk) then
                    if (sum_done = '1') then
                        long_en <= '1';
                    else
                        long_en <= '0';
                    end if;
                end if;
            end process;

            
        higher_adder_inst_3: higher_adder port map(
            clk          => clk,
            EN           => long_en,
            input       => tmp_sum,
            bias         => gate_biases,
            sum          => long_tmp,
            done         => long_done
        );
        

        scale_down_long: process(clk)
        begin
            if rising_edge(clk) then
                if long_done = '1' then
                     for i in 0 to long_tmp'length-1 loop
	for j in 0 to long_tmp(i)'length-1 loop
	scaled_down_tmp(i)(j) <= long_tmp(i)(j)/1000;
	end loop;
end loop;
                    scale_done <= '1';
                end if;
            end if;
        end process;

        activate : for i in 0 to long_tmp'length - 1 generate
            
            
        vector_activation_tanh_inst_0: vector_activation_tanh port map(
            clk    => clk,
            EN     => scale_done,
            vector => scaled_down_tmp(i),
            result => output(i),
            done   => tmp_activate_done(i)
        );
        
        end generate activate;

        process(clk)
        begin
            if tmp_activate_done(tmp_activate_done'length-1) = '1' then
                activate_done <= '1';
            end if;
        end process;

        process (clk)
        begin
        if rising_edge(clk) then
            if en = '1' then
                if activate_done = '1' then
                    done <= '1';
                end if;
            else
                done <= '0';
            end if;
        end if;
        end process;
        end architecture;
        