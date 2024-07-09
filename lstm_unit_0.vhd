
        
library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
-- use IEEE.fixed_pkg.all;

        
library work;       -- Default package name
use work.config.all;


        
        entity lstm_unit_0 is
            port(
                clk           : in std_logic;
                EN            : in std_logic;
                inputs        : in input_array;
                output        : out output_type;
                done          : out std_logic
            );
        end entity lstm_unit_0;
        

        architecture Behavioral of lstm_unit_0 is
        
        component lstm_cell is
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
        end component;
        

        signal unit1_done: std_logic;
        signal unit2_done: std_logic;
        signal unit3_done: std_logic;
        
        signal short : input_type := (0, 0, 0, 0);
        signal long  : input_type := (0, 0, 0, 0); -- consider making it input of lstm_unit or instantiate

        signal short1: input_type;
        signal long1 : input_type;

        signal short2: input_type;
        signal long2 : input_type;

        signal short3: input_type;
        signal long3 : input_type;

        -- short4 is the output so is netted to the unit output
        signal long4 : input_type;

        begin
        
        lstm_cell_inst_0: lstm_cell port map(
            clk          => clk,
            EN           => EN,
            input        => inputs(0),
            long         => long,
            short        => short,
            new_long     => long1,
            new_short    => short1,
            done         => unit1_done
        );
        
        
        lstm_cell_inst_1: lstm_cell port map(
            clk          => clk,
            EN           => unit1_done,
            input        => inputs(1),
            long         => long1,
            short        => short1,
            new_long     => long2,
            new_short    => short2,
            done         => unit2_done
        );
        
        
        lstm_cell_inst_2: lstm_cell port map(
            clk          => clk,
            EN           => unit2_done,
            input        => inputs(2),
            long         => long2,
            short        => short2,
            new_long     => long3,
            new_short    => short3,
            done         => unit3_done
        );
        
        
        lstm_cell_inst_3: lstm_cell port map(
            clk          => clk,
            EN           => unit3_done,
            input        => inputs(3),
            long         => long3,
            short        => short3,
            new_long     => long4,
            new_short    => output,
            done         => done
        );
        

    end Behavioral;
        