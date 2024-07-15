
        
library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
-- use IEEE.fixed_pkg.all;

        
library work;       -- Default package name
use work.config.all;


        
        entity candidate_gate is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                input         : in output_type;
                short         : in output_type;
                output        : out output_type;
                done          : out std_logic
            );

            -- declare and instantiate weight and biases for each gate here
            signal input_weights : weight_type := -91;
            signal gate_biases  : output_type   := 653856;
            signal short_weights : weight_type := 2971;
        end entity candidate_gate;
        

        architecture Behavioral of candidate_gate is
        
        component multiplier is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                num1, num2    : in const_int;
                prod          : out const_int;
                done          : out std_logic
            );
        end component;
        
        
        component adder is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                input         : in const_int;
                bias          : in const_int;
                sum           : out const_int;
                done          : out std_logic
            );
        end component;
        
        
        component sigmoid is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                num    : in integer;
                result : out integer;
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
        
        ------------------------------------------

        begin
            
        multiplier_inst_4: multiplier port map(
            clk   => clk,
            EN    => EN,
            num1  => input,
            num2  => input_weights,
            prod  => input_c,
            done  => input_done
        );
        
            
        multiplier_inst_5: multiplier port map(
            clk   => clk,
            EN    => EN,
            num1  => short,
            num2  => short_weights,
            prod  => short_c,
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
            
            
        adder_inst_4 : adder port map(
            clk          => clk,
            EN           => sum_en,
            input        => input_c,
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

            
        adder_inst_5 : adder port map(
            clk          => clk,
            EN           => long_en,
            input        => tmp_sum,
            bias         => gate_biases,
            sum          => long_tmp,
            done         => long_done
        );
        

        scale_down_long: process(clk)
        begin
            if rising_edge(clk) then
                if long_done = '1' then
                     scaled_down_tmp <= long_tmp/1000;
                    scale_done <= '1';
                end if;
            end if;
        end process;

        
            
        sigmoid_inst_1: sigmoid port map(
            clk    => clk,
            EN     => scale_done,
            num    => scaled_down_tmp,
            result => output,
            done   => activate_done
        );
        
            
        

        

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
        