#Inputs
roi=11.95
princ1=30

planned_repayment_yrs=7


#Fixed values
princ=princ1*100000
interest= princ*roi*14/100
total= interest+princ
permon=total/(12*14)

#foreclosure
planned_interest=princ*roi*planned_repayment_yrs/100
planned_repayment=total-(princ+planned_interest)
extra1=planned_repayment/(12*planned_repayment_yrs)
extra= permon+extra1


#prints
print("\nTotal Amt to be paid: INR "+str(int(total)))
print("\nEMI: EUR "+str(int(permon/90))+" or INR "+str(int(permon)))
print("\nFor a foreclosure in "+str(planned_repayment_yrs)+" years, amount left after initial repayment: INR "+ str(int(planned_repayment)))
print("In which case, a monthly extra of EUR "+str(int(extra1/90))+" needs to be SAVED")
print("New EMI: EUR "+str(int(extra/90))+" per month or INR "+str(int(extra))+"\n")
print("Interest per year: INR "+str(int(interest/14)))
