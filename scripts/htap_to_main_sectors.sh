#!/bin/bash

# First step in the terminal: 
# conda activate cdo
# Author: Alejandro D
# Input and output file paths

# Sectors names
h3_1='ship'       
h3_21='davi'       
h3_22='iavi'       
h3_3='ene'   
h3_41='ind'     
h3_42='fgt'     
h3_43='slv'     
h3_51='tra'      
h3_52='btw'          
h3_53='dship'      
h3_54='otra'          
h3_6='res'        
h3_7='wst'   
h3_81='agrb'    
h3_82='lvstck'   
h3_83='crops'

pathname=/p1-sto-amanan/dados_compartilhados/emis/htap_to_wrfchem

# HTAPv3_1: International Shipping --------------------------------------------

sector='others'

pollutants=('CO' 'NH3' 'NMVOC' 'NOx' 'SO2' 'PM10' 'PM2.5' 'BC' 'OC')

for pol in "${pollutants[@]}"; do
    input_file=${pathname}/edgar_HTAPv3_2018_${pol}.nc
    output_file=edgar_HTAPv3_2018_${pol}.nc
    ncap2 -h -O -s "${sector}=${h3_1}+${h3_21}+${h3_22}+${h3_3}+${h3_6}+${h3_7};" $input_file tmp.nc
    ncks -h -O -v $sector tmp.nc $output_file

    # change from netcdf4 to netcdf3
    ncks -h -O -3 $output_file $output_file
    
    rm tmp.nc
    echo "${sector} for ${pol}"
done

# HTAPv3_4: Industry ----------------------------------------------------------
# ind = h3_41 + h3_42 + h3_43
sector="ind"  # They have almost the same temporal distribution and maybe the same SCC

pollutants=('CO' 'NH3' 'NMVOC' 'NOx' 'SO2' 'PM10' 'PM2.5' 'BC' 'OC')

for pol in "${pollutants[@]}"; do
    input_file=${pathname}/edgar_HTAPv3_2018_${pol}.nc
    output_file=edgar_HTAPv3_2018_${pol}.nc
    ncap2 -h -O -s "${sector}=${h3_41}+${h3_42}+${h3_43};" $input_file tmp.nc
    ncks -h -O -v $sector tmp.nc tmp.nc
    ncks -h -A tmp.nc $output_file
    
    # change from netcdf4 to netcdf3
    ncks -h -O -3 $output_file $output_file

    rm tmp*
    echo "${sector} for ${pol}"
done

# HTAP_5: Ground transport ----------------------------------------------------
gases=('CO' 'NH3' 'NMVOC' 'NOx' 'SO2')
aerosols=('PM10' 'PM2.5' 'BC' 'OC')
sector="road_exh"
#"HTAPv3_5_1_Road_Transport"          # road transport, combustion, and evaporative
#"HTAPv3_5_2_Brake_and_Tyre_wear"     # Re-suspended dust from pavements or tyre and brake wear
#"HTAPv3_5_3_Domestic_shipping"       # inland waterways and domestic shipping
#"HTAPv3_5_4_Other_ground_transport"  # pipelines and mobile machinery

for pol in "${gases[@]}"; do
    input_file=${pathname}/edgar_HTAPv3_2018_${pol}.nc
    output_file=edgar_HTAPv3_2018_${pol}.nc
    ncap2 -h -O -s "${sector}=${h3_51}+${h3_53}+${h3_54};" $input_file tmp.nc
    ncks -h -O -v $sector tmp.nc tmp.nc
    ncks -h -A tmp.nc $output_file
    
    # change from netcdf4 to netcdf3
    ncks -h -O -3 $output_file $output_file

    rm tmp*
    echo "${sector} for ${pol}"
done

for pol in "${aerosols[@]}"; do
    input_file=${pathname}/edgar_HTAPv3_2018_${pol}.nc
    output_file=edgar_HTAPv3_2018_${pol}.nc
    ncap2 -h -O -s "${sector}=${h3_51}+${h3_53}+${h3_54};" $input_file tmp.nc
    ncks -h -O -v $sector tmp.nc tmp.nc
    ncks -h -A tmp.nc $output_file
    
    # change from netcdf4 to netcdf3
    ncks -h -O -3 $output_file $output_file

    rm tmp*
    echo "${sector} for ${pol}"
done

# Resuspension dust emissions from pavements or tyre and brake wear
sector="road_res"

for pol in "${gases[@]}"; do
    input_file=${pathname}/edgar_HTAPv3_2018_${pol}.nc
    output_file=edgar_HTAPv3_2018_${pol}.nc
    ncap2 -h -O -s "${sector}=${h3_51}*0;" $input_file tmp.nc
    ncks -h -O -v $sector tmp.nc tmp.nc
    ncks -h -A tmp.nc $output_file
    
    # change from netcdf4 to netcdf3
    ncks -h -O -3 $output_file $output_file

    rm tmp*
    echo "${sector} for ${pol}"
done

for pol in "${aerosols[@]}"; do
    input_file=${pathname}/edgar_HTAPv3_2018_${pol}.nc
    output_file=edgar_HTAPv3_2018_${pol}.nc
    ncap2 -h -O -s "${sector}=${h3_52};" $input_file tmp.nc 
    ncks -h -O -v $sector tmp.nc tmp.nc
    ncks -h -A tmp.nc $output_file
    
    # change from netcdf4 to netcdf3
    ncks -h -O -3 $output_file $output_file

    rm tmp*
    echo "${sector} ${pol}"
done

# HTAPv3_8: Agriculture -------------------------------------------------------
# agr = h3_81 + h3_82 + h3_83
sector='agr'   

pols_1=('PM10' 'PM2.5' 'BC' 'OC' 'NH3' 'NOx' 'NMVOC')
pols_2=('CO' 'SO2')

for pol in "${pols_1[@]}"; do
    input_file=${pathname}/edgar_HTAPv3_2018_${pol}.nc
    output_file=edgar_HTAPv3_2018_${pol}.nc
    ncap2 -h -O -s "${sector}=${h3_81}+${h3_82}+${h3_83};" $input_file tmp.nc
    ncks -h -O -v $sector tmp.nc tmp.nc # create variable
    ncks -h -A tmp.nc $output_file 

    # change from netcdf4 to netcdf3
    ncks -h -O -3 $output_file $output_file

    rm tmp.nc
    echo "${sector} for ${pol}"
done

for pol in "${pols_2[@]}"; do
    input_file=${pathname}/edgar_HTAPv3_2018_${pol}.nc
    output_file=edgar_HTAPv3_2018_${pol}.nc
    ncap2 -h -O -s "${sector}=${h3_81}+${h3_83};" $input_file tmp.nc
    ncks -h -O -v $sector tmp.nc tmp.nc # create variable
    ncks -h -A tmp.nc $output_file 

    # change from netcdf4 to netcdf3
    #ncks -h -O -3 $output_file $output_file

    rm tmp.nc
    echo "${sector} for ${pol}"
done


#echo "Creating PM2.5_oth = PM2.5 - (BC+OC)" # --------------------------------- 
#                                                                                
#sectors=('others' 'ind' 'road_exh' 'road_res')                                  
#                                                                                
#for sector in "${sectors[@]}"; do                                               
#    pm2_5_file=edgar_HTAPv3_2018_PM2.5.nc                                       
#    bc_file=edgar_HTAPv3_2018_BC.nc                                             
#    oc_file=edgar_HTAPv3_2018_OC.nc                                             
#    output_file=edgar_HTAPv3_2018_PM2.5_oth.nc                                  
#                                                                                
#    ncks -h -v $sector $pm2_5_file tmp_pm2_5.nc                                 
#    ncks -h -v $sector $bc_file tmp_bc.nc                                       
#    ncks -h -v $sector $oc_file tmp_oc.nc                                       
#                                                                                
#    # Perform substraction using cdo                                                                    
#    cdo sub tmp_pm2_5.nc -add tmp_bc.nc tmp_oc.nc tmp_res.nc                    
#    ncks -h -A tmp_res.nc $output_file                                          
#                                                                                                        
#    rm tmp*.nc                                                                  
#    echo "Subtraction completed for ${sector}. Output saved to $output_file"        
#done     

echo " ALL DONE "
