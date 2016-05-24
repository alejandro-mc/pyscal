PROGRAM ASSIGNMENT;

var a,b,c : integer;

var d,e : array[0 .. 5] of integer;

BEGIN

{fibonacci numbers}
d[0] := 1;
d[1] := 1;
for i := 2 to 5 do
d[i] := d[i-1] + d[i-2];



{array assignment}
{for i := 0 to 5 do
	begin
	d[i] := i * 2;
	e[i] := i * 2 + 1;
	end;}

{this is the best program ever written}
{a := 3 + 5 * 2 ;

b:= 1 + 2;

c:= a div 4;}
{if 3 > 2 then 
    c := 1;
else
	c := 0;}


{test while do}
{a:=0;

while a > 2 do 
      a:= a + 1;} 

{test do while}
{a:=1;

do a := a+1;
while a < 100 ;}

{factorial program}
{a:=10;
b:=1;
repeat
begin 
b:= b * a;
a:= a - 1;
end;
until a < 1 ;}

{for loop test}
{a := 0;
for z := 1 to 100 do
	a := a + 1;}

END.
