from Component import Component

class Configuration(Component):
    def __init__(self,input_shape, weight_shape, n_inputs):
        self.input_shape = input_shape
        self.weight_shape = weight_shape
        self.n_inputs = n_inputs

    @property
    def name(self):
        return "config"
    
    def toVHDL(self):
        arr = 0 if self.input_shape[0] == 1 and self.input_shape[1] == 1 else 1
        return f"""
        library IEEE;
        use IEEE.STD_LOGIC_1164.all;
        use IEEE.NUMERIC_STD.all;

        -- this file defines all the data types used in the project
        package config is
            subtype const_int is integer range integer'low to integer'high;
            -- input constants
            constant n_row: const_int := {self.input_shape[0]-1};
            constant n_col: const_int := {self.input_shape[1]-1};
           
            -- gate constants
            constant n_w_row : const_int := {self.weight_shape[0]-1};
            constant n_w_col : const_int := {self.weight_shape[1]-1};
            -- gate types
            {'type weight_row is array (0 to n_w_col) of const_int;' if arr else ''}
            {'type weight_type is array (0 to n_w_row) of weight_row;' if arr else "subtype weight_type is integer range integer'low to integer'high;"}
            -- output type
            {'type output_row is array(0 to n_w_row) of const_int;' if arr else ''}
            {'type output_type is array (0 to n_row) of output_row;' if arr else "subtype output_type is integer range integer'low to integer'high;"}
            type input_array is array(0 to {self.n_inputs-1}) of output_type;
        end package;
        """
        