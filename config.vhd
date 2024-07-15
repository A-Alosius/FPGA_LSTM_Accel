
        library IEEE;
        use IEEE.STD_LOGIC_1164.all;
        use IEEE.NUMERIC_STD.all;

        -- this file defines all the data types used in the project
        package config is
            subtype const_int is integer range integer'low to integer'high;
            -- input constants
            constant n_row: const_int := 0;
            constant n_col: const_int := 0;
            -- input types
            
            subtype input_type is integer range integer'low to integer'high;
            
            -- gate constants
            constant n_w_row : const_int := 0;
            constant n_w_col : const_int := 0;
            -- gate types
            
            subtype weight_type is integer range integer'low to integer'high;
            -- output type
            
            subtype output_type is integer range integer'low to integer'high;
            type input_array is array(0 to 3) of output_type;
        end package;
        