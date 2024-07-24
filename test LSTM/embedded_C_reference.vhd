-- Code your testbench here
library IEEE;
use work.dtypes.all;
use IEEE.std_logic_1164.all;
use IEEE.NUMERIC_STD.ALL;
use work.config.all;


entity test_unit is

end entity;

architecture behavioral of test_unit is
component communication_module is
	port(
    	 clk 	  : in std_logic;
         mcu_clk  : in std_logic;
         en 	  : in std_logic;
         rst	  : in std_logic;
         ctrl 	  : in std_logic_vector(1 downto 0);
    	 inbits   : in std_logic_vector(9 downto 0); -- to be decided by user
         outbits  : out std_logic_vector(9 downto 0)
    	);
end component;

signal clk : std_logic := '0';
signal mcu_clk : std_logic := '0';
signal en  : std_logic := '0';
signal inbits : std_logic_vector(9 downto 0);
signal ctrl : std_logic_vector(1 downto 0);
signal output : std_logic_vector(9 downto 0);
signal rst : std_logic := '0';
signal don: std_logic := '0';

begin
u1 : communication_module port map(clk=>clk, mcu_clk=>mcu_clk, en=>en, rst=>rst, ctrl=>ctrl, inbits=>inbits, outbits=> output);

process
-- MCU SIDE
begin
	mcu_clk <= '0';
    wait for 100 ns;
    
	mcu_clk <= not(mcu_clk);
    wait for 100 ns;
    if ctrl = "01" and rst = '0' then
    	inbits <= "0000000000"; -- 9
    end if;
    wait for 100 ns;
    
    mcu_clk <= '0';
    wait for 100 ns;
    
	mcu_clk <= not(mcu_clk);
    wait for 100 ns;
    if ctrl = "01" and rst = '0' then
    	inbits <= "0011111010"; -- 9
    end if;
    wait for 100 ns;
    
    mcu_clk <= '0';
    wait for 100 ns;
    
	mcu_clk <= not(mcu_clk);
    wait for 100 ns;
    if ctrl = "01" and rst = '0' then
    	inbits <= "0111110100"; -- 9
    end if;
    wait for 100 ns;
    
    mcu_clk <= '0';
    wait for 100 ns;
    
	mcu_clk <= not(mcu_clk);
    wait for 100 ns;
    if ctrl = "01" and rst = '0' then
    	inbits <= "1111101000"; -- 9
    end if;
    wait for 100 ns;
end process;

process
-- FPGA SIDE
    begin 
    
          ---------------------------get inputs-------------------------------------------------
          clk <= '0';
          en <= '0';
          rst <= '0';
          ctrl <= "00";
          
          wait for 50 ns;
          
          clk <= not(clk);
          en <= not en;
          wait for 50 ns;
          
          clk <= not(clk);
          en <= not en;
		  wait for 50 ns;
          
          clk <= not(clk);
          en <= not(en);
          if rst = '0' then
          	ctrl <= "01";
--           	inbits <= "0000000000"; -- 9 
          end if;
          wait for 1300 ns;
          
          clk <= not(clk);
          en <= not en;
          wait for 50 ns;
          
          clk <= not(clk);
          en <= not en;
          wait for 50 ns;
          
          
          
          clk <= not(clk);
          en <= not en;
          wait for 50 ns;
          
          clk <= not(clk);
          en <= not en;
          if rst = '0' then
--           	inbits <= "0011111010"; -- 9 + 3
          end if;
          wait for 50 ns;
          
          clk <= not(clk);
          en <= not en;
          wait for 50 ns;
          
          clk <= not(clk);
          en <= not en;
          if rst = '0' then
--           	inbits <= "0111110100"; -- 12 + 1
          end if;
          wait for 50 ns;
          
          clk <= not(clk);
          en <= not en;
          wait for 50 ns;
          
          clk <= not(clk);
          en <= not en;
          if rst = '0' then
--           	inbits <= "1111101000"; -- 13 + 2
          end if;
          wait for 50 ns;
          
          clk <= not(clk);
          en <= not en;
          wait for 50 ns;
          
          clk <= not(clk);
          en <= not en;
          wait for 50 ns;
          
          
          ----------------------------- pass inputs for inference--------------------------------------
          
          clk <= not(clk);
          en <= not en;
          if rst = '0' then
          	ctrl <= "00";
          end if;
          wait for 50 ns;
          
          clk <= not(clk);
          en <= not en;
          if rst = '0' then
          	ctrl <= "10";
          end if;
          wait for 50 ns;
          
          clk <= not(clk);
          en <= not en;
          wait for 50 ns;
          
          clk <= not(clk);
          en <= not en;
          wait for 50 ns;
          
          
          
          
       
          
          ------------------------------ convert response to bits and output ----------------------------
           clk <= not(clk);
          en <= not en;
          wait for 50 ns;
          
          clk <= not(clk);
          en <= not en;
          if rst = '0' then
          	ctrl <= "11"; 
          end if;
          wait for 50 ns;
          
          clk <= not(clk);
          en <= not en;
          wait for 50 ns;
          
          clk <= not(clk);
          en <= not en;
          wait for 50 ns;
          
          clk <= not(clk);
          en <= not en;
          wait for 50 ns;
          
          clk <= not(clk);
          en <= not en;
          wait for 50 ns;
          
--           rst <= '1';
          wait for 50 ns;
          

    end process;

end behavioral;