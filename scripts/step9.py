import numpy as np

#Load file
file=np.loadtxt("ph3-asp6-new.dat",comments=["#","@"])

#Assign three columns to three variables
time=file[:,0]
lambdas=file[:,1]
chi=file[:,2]


#Partial charge of side chain

q_ASP_HD1 = 0.44 * lambdas * (1 - lambdas) * (1 - chi)
#
q_ASP_HD2 = 0.44 * (1 - lambdas) * (1 - lambdas) * (1 - chi)


#q_GLU_HE1 = 0.44 * lambdas * (1 - lambdas) * (1 - chi)
#
#q_GLU_HE2 = 0.44 * (1 - lambdas) * (1 - lambdas) * (1 - chi)


#q_HSD_HD1 = 0.44 * lambdas * (1 - lambdas) * (1 - chi) + (0.44 - 0.12 * lambdas) * lambdas + 0.44 * (1 - lambdas)**2 + (0.44 - 0.12 * lambdas) * (1 - lambdas) * (1 - chi)

#q_HSE_HE2 = 0.44 * (1 - lambdas)**2 * (1 - chi) + (0.44 - 0.12 * lambdas) * (1 - lambdas) + 0.44 * lambdas * (1 - lambdas) + (0.44 - 0.12 * lambdas) * lambdas * (1 - chi)


#Create empty array with final size (2 columns more)
final=np.zeros((file.shape[0],file.shape[1]+2))

#First part of the array is equal to the original file
#final[:,0]=file[:,0]
#final[:,1]=file[:,1]
#final[:,2]=file[:,2]

final[:,:-2]=file
#Last column is U_mod
final[:,-1]= q_ASP_HD2
final[:,-2]= q_ASP_HD1
#
#final[:,-1]= q_GLU_HE2
#final[:,-2]= q_GLU_HE1

#final[:,-1]= q_HSE_HE2
#final[:,-2]= q_HSD_HD1

#Save it with numbers represented as floats with 3 decimal places
np.savetxt("ph3-asp6-charge.dat",final,header="Time lambda Chi q_ASP_HD1 q_ASP_HD2", fmt="%.5f")

#np.savetxt("ph7-glu10-charge.dat",final,header="Time lambda Chi q_GLU_HE1 q_GLU_HE2", fmt="%.5f")

#np.savetxt("ph3-asp6-charge.dat",final,header="Time lambda Chi q_HSP_HD1 q_HSP_HE2", fmt="%.5f")


#mean value of q

#dq_HD1 = np.mean(q_ASP_HD1)
#print("Mean of partial charge of HD1 is:",dq_HD1)
#sd_HD1 = np.std(q_ASP_HD1)
#print("SD of HD1 is: ",sd_HD1)


#dq_HD2 = np.mean(q_ASP_HD2)
#print("Mean of partial charge of HD2 is:",dq_HD2)
#sd_HD2 = np.std(q_ASP_HD2)
#print("SD of HD2:",sd_HD2)


#dq_ASP = np.mean(q_ASP)
#print("Mean of partial charge of ASP is:", dq_ASP)
#sd_ASP = np.std(q_ASP)
#print("SD of ASP:",sd_ASP)


