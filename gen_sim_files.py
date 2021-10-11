mod_string = """
# Model describing a 2D tissue with cells growing and dividing
# Growth is exponential and homogeneous, walls grow and have elasticity
# Division is along shortest path
#
# More information on tissue software http://gitlab.com/slcu/teamhj/tissue
# More information on model reactions tissue/docs/html/index.html
# Model creator henrik.jonsson@slcu.cam.ac.uk
#
4		   # number of reactions, including growth and mechanical updates
2 		   # number of division/removal rules
0 		   # number of directions (with update rules)

# ------------- growth rules ------------------

MoveVertexRadially # growth generating forces moving cell vertices outwards to generate homogeneous growth
2 0 		   # 2 parameters and 0 variables
# --- parameters
0.001		   # 0.001 k_growth. growth rate
1		   # r_pow. if r_pow=1, the distance moved is proportional to
		   # the distance of the vertex to the center (exponential growth)
		   # if r_pow=0, the vertex distance moved is constant (linear growth)

WallGrowth::Stress # irreversible growth of walls (edges), Updates wall lengths depending on stress/strain
4 2 1 1 	   # 4 parameters, 2 types of variables, 1 of each
# --- parameters
0.01		   # k_growth, irreversible growth rate
0.05		   # stress_threshold for when growth happens, cf Lockhart
1		   # stretch_flag, 0 for stress (read from wall variable), 1 for strain
1		   # linear_flag, 0 constant, 1 prop to wall length
# --- indices
0		   # wall length
1		   # stress variable (not used if stretch_flag=1)

# ------------ mechanical rules ------------

VertexFromWallSpring # Updates vertices from an asymmetric wall (edge) spring potential
2 1 1 		     # 2 parameters 1 type of variable and single variable
# --- parameters
%f		     # k_force, spring constant 0.1
1.0		     # frac_adhesion, additional strength for spring compression
# --- indices
0		     # wall length

# --- 'Ad hoc' rule to make the tissue centered at origo ---

CenterCOM 0 0

# ------- division/removal rules ----------

Division::ShortestPath2DRandomized   # Divides cells at threshold size and alon shortest path
6 1 1			   # 4 parameters, 1 variable type where 1 variable is given
# --- parameters
40			   # 40 V_threshold, size threshold for when division is triggered
1.0			   # LWall_frac, resting length of new wall in relation to real size
%f			   # Lwall_threshold, fraction of wall for avoiding old vertices
1			   # COM_flag, defining division through COM (flag=1) or random
%f			   # Fraction of time that a cell randomly divides instead of at volume threshhold.
%f			   # Fraction of time that a cell division is random instead of shortest path.
# --- indices
3			     # cell volume index (not a concentration and hence needs to be divided
			     # according to daughter cell sizes)

RemovalOutsideRadius 	     # Remove cells outside a specified radius
1 0			     # 1 parameter and 0 riables
# --- parameters
60.0			     # R_threshold, radius outside which cells are removed
"""
for ii,k_force in enumerate([.1,.3,1.0,3.0]):
    for jj,LWt in enumerate([.1,.3,.6]):
        for kk,randFreq in enumerate([-1.0,.00001,.00003,.0001]):
            for ll,randDivFreq in enumerate([-1.0,.01,.03,.1,.5,1.0]):
                with open("modelfiles/s%d_s%d_s%d_s%d.model"%(ii,jj,kk,ll),'w') as f:
                    f.write(mod_string % (k_force,LWt,randFreq,randDivFreq))
                for mm in range(1,2):
                    print(ii,jj,kk,ll,mm)
