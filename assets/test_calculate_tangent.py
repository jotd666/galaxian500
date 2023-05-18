# generates test cases for this routine
# insert at startup (galaxian_reset). If osd_break is
# call, check testcase in d1, and expected values in the code
tests = (("69,A5,53"),
("69,A4,53"),
("68,96,5A"),
("1F,62,2B"),
("1D,5F,2B"),
("13,51,1F"),
("0D,49,19"),
("50,99,44"),
)

def write(m):
    print(m,end="")

for i,t in enumerate(tests):
    a,d,c = t.split(",")
    write(f"""\tmove.b   #0x{a},d0
    move.b  #0x{d},d3
    bsr     CALCULATE_TANGENT
    cmp.b   #0x{c},d2
    beq.b   0f
    move.b  #{i},d1
    jsr     osd_break
0:
""")