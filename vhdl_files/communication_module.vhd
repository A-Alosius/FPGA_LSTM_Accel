
        
library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
-- use IEEE.fixed_pkg.all;

        
library work;       -- Default package name
use work.config.all;

        
        entity communication_module is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                rst    : in std_logic;
                ctrl   : in std_logic_vector(1 downto 0);
                inbits : in std_logic_vector(9 to 0);
                outbits: out std_logic_vector(9 to 0)
                );
        end communication_module;
        

        architecture Behavioral of communication_module is
        
        Component lstm_unit_0 is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                inputs        : in input_array;
                output        : out output_type;
                done          : out std_logic
            );
        end component;
        
        
        component num2bin is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                number : in const_int;
                bits   : out std_logic_vector(9 downto 0);
                done   : out std_logic
            );
        end component;
        
        
        component input_picker is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                inbits : in std_logic_vector(9 downto 0);
                output : out input_array;
                done   : out std_logic
            );
        end component;
        

        -- relevant signals
        signal input_arr 	   	 : input_array;

        signal lstm_unit_pre_en  : std_logic;
        signal lstm_en    	     : std_logic;
        signal lstm_unit_done  	 : std_logic;

        signal bin2num_en      	 : std_logic;
        signal num2bin_pre_en	 : std_logic;
        signal num2bin_en	  	 : std_logic;
        signal bin2num_done    	 : std_logic; -- not really necessary here, should go in input_picker
        signal num2bin_done      : std_logic;
        signal inputs_ready    	 : std_logic;

        signal input_picker_en	 : std_logic;
        signal input_picker_done : std_logic;

        signal tmp_num 			 : integer;

        signal output 			 : integer;
        signal sum_done			 : std_logic;

        begin
            process(clk)
            begin
                -- reset is done on mcu side.
                -- if you reset, set ctrl_signal to idle too
                
                if rst = '1' then
                    null;
                else
                    if rising_edge(clk) then
                        if en = '1' then
                            case ctrl_sig is
                                -- idle: just maintain signals
                                when "00" => 
                                    null;

                                -- recv input
                                when "01" => 
                                    lstm_unit_pre_en  <= '0';
                                    input_picker_en   <= '1';
                                    num2bin_pre_en    <= '0';

                                -- run inference happens when inputs are ready
                                when "10" => 
                                    lstm_unit_pre_en  <= '1';
                                    num2bin_pre_en    <= '0';
                                    input_picker_en   <= '0';

                                -- output result convert num to bin and send to appropriate pins then maintain signal with idle
                                when "11" => 
                                    lstm_unit_pre_en  <= '0';
                                    num2bin_pre_en    <= '1';
                                    input_picker_en   <= '0';

                                when others =>
                                    lstm_unit_pre_en  <= '0';
                                    num2bin_pre_en 	  <= '0';
                                    input_picker_en   <= '0';
                            end case;
                        end if;
                    end if;
                end if;  
            end process;
    
            inputs_ready_infer : process (clk)
            begin
                if rising_edge(clk) then
                    if en = '1' then
                        if input_picker_done = '1' and lstm_unit_pre_en = '1' then
                            lstm_en <= '1';
                        end if;
                    end if;
                end if;
            end process;

            
        input_picker_inst: input_picker port map(
            clk    => clk,
            EN     => input_picker_en,
            inbits => inbits,
            output => input_arr,
            done   => input_picker_done
        );
        
            
        lstm_unit_0_inst: lstm_unit_0 port map(
            clk   => clk,
            EN    => lstm_en,
            inputs=> input_arr,
            output=> output,
            done  => lstm_unit_done
        );
        
   
            output_ready_generate_bits : process(clk)
            begin
                if rising_edge(clk) then
                    if en = '1' then
                        if num2bin_pre_en = '1' and lstm_unit_done = '1' then
                            num2bin_en <= '1';
                        end if;
                    end if;
                end if;
            end process;

            
        num2bin_inst: num2bin port map(
            clk    => clk,
            EN     => num2bin_en,
            number => output,
            bits   => outbits,
            done   => num2bin_done
        );
        
        end behavioral;
        