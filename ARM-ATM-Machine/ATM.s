@ ------------------------------------------------
@ Start instruction section

.text
.global main

main:

INIT: 
 mov r5, #50@ $20 bills
 mov r6, #50 @$10 bills
 mov r7, #10 @Customer limit

LOOP:
@Check custmoer limit
 mov r10, #0 @Number of 10 bills
 mov r11, #0 @number of 20 bills
 cmp r7, #0
 beq customerLimit @Branch if limit reached.
        @ Use printf to print input prompt
        LDR r0, =input_prompt   @ string to print needs to be in r0
        BL printf               @ call printf

        @ use scanf to read an integer from the user
        @ r0 must contain address of the input format string
        @ r1 must contain address of the variable where input will be stored
        LDR r0, =input_format
        LDR r1, =intval
        BL scanf                @ Get INPUT

        @ Move the value to print into r1
        LDR r2, =intval
        LDR r1, [r2]
 @Input is now in r1
 mov r9, r1
 mov r8, r1
 b CHECKINPUT

inputReturn: @So, now we know we have a legit input, which is in r1
 sub r7, r7, #1 @One customer used
b dispenseCash
 dispenseCashReturn:
        

        @ Load the output format string
        @ Value to print is already in r1
        LDR r0, =output_format
        BL printf               @ call printf
 END:
        @ exit the program
        MOV r7, #1
        SVC 0

CHECKINPUT:
 cmp r8, #200
 bgt requestInvalid
 cmp r9, #0
 sub r9, r9, #10
 blt inputError
 beq inputReturn
 b CHECKINPUT

inputError:
 LDR r0, =inputErrorMessage
 BL printf
 b LOOP

customerLimit:
 LDR r0, =customerLimitMessage
 BL printf
 b END

dispenseCash:
 cmp r8, #0
 beq Report @print return
 b countMoney
 countMoneyReturn:

 cmp r5, #0
 beq tenDollarBill @Because we're out of $20s
 cmp r8, #10
 beq tenDollarBill @Only need a ten dollar bill

 b twentyDollarBill

tenDollarBill: @Dispense one bill
 cmp r6, #0
 beq OUT
 add r10, r10, #1
 sub r6, #1
 sub r8, #10
 b dispenseCash

twentyDollarBill: @Dispence one bill
 sub r5, #1
 sub r8, #20
 add r11, r11, #1
 b dispenseCash

Report: @Where we tell them how many bills we gave them.
 mov r1, r11
 LDR r0, =cashReport1
 BL printf

 mov r1, r10
 LDR r0, =cashReport2
 BL printf

 b LOOP

OUT: @For if we are out of $10s
 LDR r0, =outMessage
 BL printf
 b END

countMoney: 
 mov r2, #0
 mov r3, r5
 mov r4, r6
 @Init variables

countLoop:
 cmp r3, #0 @Check num of $20s
 cmpeq r4, #0 @Check num of $10s
 beq notEnoughMoney
 cmp r2, #200
 @bgt requestInvalid

 @Branch if we have the amount we need
 cmp r2, r8
 bge countMoneyReturn

 @And if we do want to add a number...

 @Adds a $10 bill
 sub r4, #1
 add r2, r2, #10

 cmp r3, #0
 subgt r3, #1
 addgt r2, r2, #20

 b countLoop

notEnoughMoney:
 LDR r0, =notEnoughMoneyMessage
 BL printf
 b LOOP

requestInvalid:
 LDR r0, =Invalid
 BL printf
 b LOOP


@ ------------------------------------------------
@ Start data section

.data

@ You're going to need null terminated strings (use .asciz)
input_prompt: .asciz "Enter how much cash you wish to withdrawl: "
output_format: .asciz "Integer + 1: %d:\n"

notEnoughMoneyMessage: .asciz "*The machine does not have enough cash for your withdrawl.* \n*Please try again with a lower amount.*\n"

cashReport1: .asciz "Number of $20 bills given: %d\n"
Invalid: .asciz "\n*You may not withdrawl more than $200.*\n\n"
cashReport2: .asciz "Number of $10 bills given: %d:\n"

outMessage: .asciz "*This machine is out of money. Please come again tomorrow.*\n"
customerLimitMessage: .asciz "*Daily customer limit reached. Please come again tomorrow.*\n"
inputErrorMessage: .asciz "    **ERROR**\n\n Not a valid withdrawl amount.\n\n"
input_format: .asciz "%d"

.align 4

@ Set aside space for an integer
intval: .word 0

	
