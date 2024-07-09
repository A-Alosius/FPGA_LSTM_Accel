
        library IEEE;
        use IEEE.STD_LOGIC_1164.all;
        use IEEE.NUMERIC_STD.all;

        -- this file defines all the data types used in the project
        package config is
            subtype const_int is integer range integer'low to integer'high;
            -- input constants
            constant n_row: const_int := 0;
            constant n_col: const_int := 3;
            -- input types
            type input_row is array (0 to n_col) of const_int;
            type input_type is array (0 to n_row) of input_row;
            type input_array is array(0 to 3) of input_type;
            -- gate constants
            constant n_w_row : const_int := 3;
            constant n_w_col : const_int := 3;
            -- gate types
            type weight_row is array (0 to n_w_col) of const_int;
            type weight_type is array (0 to n_w_row) of weight_row;
            -- output type
            type output_row is array(0 to n_w_row) of const_int;
            type output_type is array (0 to n_row) of output_row;
        end package;
        