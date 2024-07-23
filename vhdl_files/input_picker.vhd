
        
library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
-- use IEEE.fixed_pkg.all;

        
library work;       -- Default package name
use work.config.all;

        
        entity input_picker is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                inbits : in std_logic_vector(9 downto 0);
                output : out input_array;
                done   : out std_logic
            );
        end input_picker;
        

        architecture Behavioral of input_picker is
        
        component bin2num is
            port (
                clk    : in std_logic;
                en     : in std_logic;
                bits   : in std_logic_vector(9 downto 0);
                number : out const_int;
                done   : out std_logic
            );
        end component;
        
            signal index : integer := 0;
            signal all_in : std_logic := '0';
            signal num : integer;
            signal bin2num_done : std_logic;

            begin
                
        bin2num_inst: bin2num port map(
            clk    => clk,
            EN     => en,
            bits   => inbits,
            number => num,
            done   => bin2num_done
        );
        
                process(clk)
                begin
                    if rising_edge(clk) then
                        if en = '1' and all_in = '0' and num > -2147483648 then
                            output(index) <= num;
                            index <= index + 1;
                            if index = 3 then
                                done <= '1';
                                all_in <= '1';
                            else
                                done <= '0';
                            end if;
                        end if;
                    end if;
                end process;
        end behavioral;
        