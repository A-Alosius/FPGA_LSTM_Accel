How to Use Library
This document provides instructions on how to use the Library
Examples are provided in each class for reference

Having your LSTM parameters ready, do the following
1- Create an instance of the LSTM2VHDL class and pass in the required parameters
    the accuracy and dp set the accuracy of the activation function and general computations respectively
    - Your gate data need to be integers. You can use the input_format method provided with the LSTM2VHDL class to scale your inputs if they are a list of floats
    - If you used tensors, kindly adjust the code to convert tensors to item before passing them to the instance of the LSTM2VHDL class
    
2- Run your code

3- You're done. Browse the vhdl_files folder in your current directory

4- Import the generated files to your synthesis tool and ensure you adjust the ports in the top level entity to match your FPGA board


THank you for using this library. Reach out to us on github at akontehalosius if you need assistance or have any suggestions

Note: Currently, the communication module is being updates to enable communication of matrix inputs for multidimensional inputs
Watch out for the new release