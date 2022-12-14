from numpy import nan

dict_MSSubClass = {
    '1-STORY 1946 & NEWER ALL STYLES': 20,
    '1-STORY 1945 & OLDER':30,
    '1-STORY W/FINISHED ATTIC ALL AGES':40,
    '1-1/2 STORY - UNFINISHED ALL AGES':45,
    '1-1/2 STORY FINISHED ALL AGES':50,
    '2-STORY 1946 & NEWER':60,
    '2-STORY 1945 & OLDER':70,
    '2-1/2 STORY ALL AGES':75,
    'SPLIT OR MULTI-LEVEL':80,
    'SPLIT FOYER':85,
    'DUPLEX - ALL STYLES AND AGES':90,
    '1-STORY PUD (Planned Unit Development) - 1946 & NEWER':120,
    '1-1/2 STORY PUD - ALL AGES':150,
    '2-STORY PUD - 1946 & NEWER':160,
    'PUD - MULTILEVEL - INCL SPLIT LEV/FOYER':180,
    '2 FAMILY CONVERSION - ALL STYLES AND AGES':190
}
#%%

#%%
dict_MSZoning = {
    'Commercial':'C (all)',
    'Floating Village Residential':'FV',
    'Residential High Density':'RH',
    'Residential Low Density':'RL',
    'Residential Medium Density':'RM'
}
#%%
dict_Street = {
    'Gravel':'Grvl',
    'Paved':'Pave'
}
#%%
dict_Alley = {
    'Gravel':'Grvl',
    'Paved':'Pave',
    'No alley access': nan
}
#%%
dict_LotShape = {
    'Regular':'Reg',
    'Slightly irregular':'IR1',
    'Moderately Irregular':'IR2',
    'Irregular':'IR3'
}
#%%
dict_LandContour = {
    'Near Flat/Level':'Lvl',
    'Banked - Quick and significant rise from street grade to building':'Bnk',
    'Hillside - Significant slope from side to side':'HLS',
    'Depression':'Low'
}
#%%
dict_Utilities = {
    'All public Utilities (E,G,W,& S)':'AllPub',
    'Electricity and Gas Only':'NoSeWa',
}
#%%
dict_LotConfig = {
    'Inside lot':'Inside',
    'Corner lot':'Corner',
    'Cul-de-sac':'CulDSac',
    'Frontage on 2 sides of property':'FR2',
    'Frontage on 3 sides of property':'FR3'
}
#%%
dict_LandSlope = {
    'Gentle slope':'Gtl',
    'Moderate Slope':'Mod',
    'Severe Slope':'Sev'
}
#%%
dict_Neighborhood = {
    'Bloomington Heights':'Blmngtn',
    'Bluestem':'Blueste',
    'Briardale':'BrDale',
    'Brookside':'BrkSide',
    'Clear Creek':'ClearCr',
    'College Creek':'CollgCr',
    'Crawford':'Crawfor',
    'Edwards':'Edwards',
    'Gilbert':'Gilbert',
    'Iowa DOT and Rail Road':'IDOTRR',
    'Meadow Village':'MeadowV',
    'Mitchell':'Mitchel',
    'North Ames':'Names',
    'Northridge':'NoRidge',
    'Northpark Villa':'NPkVill',
    'Northridge Heights':'NridgHt',
    'Northwest Ames':'NWAmes',
    'Old Town':'OldTown',
    'South & West of Iowa State University':'SWISU',
    'Sawyer':'Sawyer',
    'Sawyer West':'SawyerW',
    'Somerset':'Somerst',
    'Stone Brook':'StoneBr',
    'Timberland':'Timber',
    'Veenker':'Veenker'
}
#%%
dict_Condition1 = {
    'Adjacent to arterial street':'Artery',
    'Adjacent to feeder street':'Feedr',
    'Normal':'Norm',
    'Within 200\'\ of North-South Railroad':'RRNn',
    'Adjacent to North-South Railroad':'RRAn',
    'Near positive off-site feature--park, greenbelt, etc.':'PosN',
    'Adjacent to postive off-site feature':'PosA',
    'Within 200\'\ of East-West Railroad':'RRNe',
    'Adjacent to East-West Railroad':'RRAe'
}
#%%
dict_Condition2 = {
    'Adjacent to arterial street':'Artery',
    'Adjacent to feeder street':'Feedr',
    'Normal':'Norm',
    'Within 200\'\ of North-South Railroad':'RRNn',
    'Adjacent to North-South Railroad':'RRAn',
    'Near positive off-site feature--park, greenbelt, etc.':'PosN',
    'Adjacent to postive off-site feature':'PosA',
    'Adjacent to East-West Railroad':'RRAe'
}
#%%
dict_BldgType = {
    'Single-family Detached':'1Fam',
    'Two-family Conversion; originally built as one-family dwelling':'2FmCon',
    'Townhouse End Unit':'TwnhsE',
    'Townhouse Inside Unit':'Twnhs'
}
#%%
dict_HouseStyle = {
    'One story':'1Story',
    'One and one-half story: 2nd level finished':'1.5Fin',
    'One and one-half story: 2nd level unfinished':'1.5Unf',
    'Two story':'2Story',
    'Two and one-half story: 2nd level finished':'2.5Fin',
    'Two and one-half story: 2nd level unfinished':'2.5Unf',
    'Split Foyer':'SFoyer',
    'Split Level':'SLvl'
}
#%%
dict_OverallQual = {
    'Very Excellent':10,
    'Excellent':9,
    'Very Good':8,
    'Good':7,
    'Above Average':6,
    'Average':5,
    'Below Average':4,
    'Fair':3,
    'Poor':2,
    'Very Poor':1
}
#%%
dict_OverallCond = {
    'Excellent':9,
    'Very Good':8,
    'Good':7,
    'Above Average':6,
    'Average':5,
    'Below Average':4,
    'Fair':3,
    'Poor':2,
    'Very Poor':1
}
#%%
dict_RoofStyle = {
    'Gabrel':'Gambrel',
}
#%%
dict_RoofMatl = {
    'Clay or Tile':'ClyTile',
    'Standard (Composite) Shingle':'CompShg',
    'Membrane':'Membran',
    'Gravel & Tar':'Tar&Grv',
    'Wood Shakes':'WdShake',
    'Wood Shingles':'WdShngl'
}
#%%
dict_Exterior1st = {
    'Asbestos Shingles':'AsbShng',
    'Asphalt Shingles':'AsphShn',
    'Brick Common':'BrkComm',
    'Brick Face':'BrkFace',
    'Cinder Block':'CBlock',
    'Cement Board':'CemntBd',
    'Hard Board':'HdBoard',
    'Imitation Stucco':'ImStucc',
    'Metal Siding':'MetalSd',
    'Plywood':'Plywood',
    'Stone':'Stone',
    'Stucco':'Stucco',
    'Vinyl Siding':'VinylSd',
    'Wood Siding':'Wd Sdng',
    'Wood Shingles':'WdShing'
}
#%%
dict_Exterior2nd = {
    'Asbestos Shingles':'AsbShng',
    'Asphalt Shingles':'AsphShn',
    'Brick Common':'BrkComm',
    'Brick Face':'BrkFace',
    'Cinder Block':'CBlock',
    'Cement Board':'CemntBd',
    'Hard Board':'HdBoard',
    'Imitation Stucco':'ImStucc',
    'Metal Siding':'MetalSd',
    'Other':'Other',
    'Plywood':'Plywood',
    'Stone':'Stone',
    'Stucco':'Stucco',
    'Vinyl Siding':'VinylSd',
    'Wood Siding':'Wd Sdng',
    'Wood Shingles':'WdShing'
}
#%%
dict_MasVnrType = {
    'Brick Common':'BrkCmn',
    'Brick Face':'BrkFace',
    'None':'None',
    'Stone':'Stone'
}
#%%
dict_ExterQual = {
    'Excellent':'Ex',
    'Good':'Gd',
    'Average/Typical':'TA',
    'Fair':'Fa',
}
#%%
dict_ExterCond = {
    'Excellent':'Ex',
    'Good':'Gd',
    'Average/Typical':'TA',
    'Fair':'Fa',
    'Poor':'Po'
}
#%%
dict_Foundation = {
    'Brick & Tile':'BrkTil',
    'Cinder Block':'CBlock',
    'Poured Contrete':'PConc',
    'Slab':'Slab',
    'Stone':'Stone',
    'Wood':'Wood'
}
#%%
dict_BsmtQual = {
    'Excellent (100+ inches)':'Ex',
    'Good (90-99 inches)':'Gd',
    'Typical (80-89 inches)':'TA',
    'Fair (70-79 inches)':'Fa',
    'No Basement':nan
}
#%%
dict_BsmtCond = {
    'Good':'Gd',
    'Typical':'TA',
    'Fair':'Fa',
    'Poor':'Po',
    'No Basement':nan
}
#%%
dict_BsmtExposure = {
    'Good Exposure':'Gd',
    'Average Exposure (split levels or foyers typically score average or above)':'Av',
    'Mimimum Exposure':'Mn',
    'No Exposure':'No',
    'No Basement':nan
}
#%%
dict_BsmtFinType1 = {
    'Good Living Quarters':'GLQ',
    'Average Living Quarters':'ALQ',
    'Below Average Living Quarters':'BLQ',
    'Average Rec Room':'Rec',
    'Low Quality':'LwQ',
    'Unfinshed':'Unf',
    'No Basement':nan
}
#%%
dict_BsmtFinType2 = {
    'Good Living Quarters':'GLQ',
    'Average Living Quarters':'ALQ',
    'Below Average Living Quarters':'BLQ',
    'Average Rec Room':'Rec',
    'Low Quality':'LwQ',
    'Unfinshed':'Unf',
    'No Basement':nan
}
#%%
dict_Heating = {
    'Floor Furnace':'Floor',
    'Gas forced warm air furnace':'GasA',
    'Gas hot water or steam heat':'GasW',
    'Gravity furnace':'Grav',
    'Hot water or steam heat other than gas':'OthW',
    'Wall furnace':'Wall'
}
#%%
dict_HeatingQC = {
    'Excellent':'Ex',
    'Good':'Gd',
    'Average/Typical':'TA',
    'Fair':'Fa',
    'Poor':'Po'
}
#%%
dict_CentralAir = {
    'No':'N',
    'Yes':'Y'
}
#%%
dict_Electrical = {
    'Standard Circuit Breakers & Romex':'SBrkr',
    'Fuse Box over 60 AMP and all Romex wiring (Average)':'FuseA',
    '60 AMP Fuse Box and mostly Romex wiring (Fair)':'FuseF',
    '60 AMP Fuse Box and mostly knob & tube wiring (poor)':'FuseP',
    'Mixed':'Mix'
}
#%%
dict_KitchenQual = {
    'Excellent':'Ex',
    'Good':'Gd',
    'Typical/Average':'TA',
    'Fair':'Fa'
}
#%%
dict_Functional = {
    'Typical Functionality':'Typ',
    'Minor Deductions 1':'Min1',
    'Minor Deductions 2':'Min2',
    'Moderate Deductions':'Mod',
    'Major Deductions 1':'Maj1',
    'Major Deductions 2':'Maj2',
    'Severely Damaged':'Sev'
}
#%%
dict_FireplaceQu = {
    'Excellent - Exceptional Masonry Fireplace':'Ex',
    'Good - Masonry Fireplace in main level':'Gd',
    'Average - Prefabricated Fireplace in main living area or Masonry Fireplace in basement':'TA',
    'Fair - Prefabricated Fireplace in basement':'Fa',
    'Poor - Ben Franklin Stove':'Po',
    'No Fireplace':nan
}
#%%
dict_GarageType = {
    'More than one type of garage':'2Types',
    'Attached to home':'Attchd',
    'Basement Garage':'Basment',
    'Built-In (Garage part of house - typically has room above garage)':'BuiltIn',
    'Car Port':'CarPort',
    'Detached from home':'Detchd',
    'No Garage':nan
}
#%%
dict_GarageFinish = {
    'Finished':'Fin',
    'Rough Finished':'RFn',
    'Unfinished':'Unf',
    'No Garage':nan
}
#%%
dict_GarageQual = {
    'Excellent':'Ex',
    'Good':'Gd',
    'Typical/Average':'TA',
    'Fair':'Fa',
    'Poor':'Po',
    'No Garage':nan
}
#%%
dict_GarageCond = {
    'Excellent':'Ex',
    'Good':'Gd',
    'Typical/Average':'TA',
    'Fair':'Fa',
    'Poor':'Po',
    'No Garage':nan
}
#%%
dict_PavedDrive = {
    'Paved':'N',
    'Partial Pavement':'P',
    'Dirt/Gravel':'N'
}
#%%
dict_PoolQC = {
    'Excellent':'Ex',
    'Good':'Gd',
    'Fair':'Fa',
    'No Pool':nan
}
#%%
dict_Fence = {
    'Good Privacy':'GdPrv',
    'Minimum Privacy':'MnPrv',
    'Typical/Average':'GdWo',
    'Fair':'MnWw',
    'No Fence':nan
}
#%%
dict_MiscFeature = {
    '2nd Garage (if not described in garage section)':'Gar2',
    'Other':'Othr',
    'Shed (over 100 SF)':'Shed',
    'Tennis Court':'TenC',
    'None':nan
}
#%%
dict_SaleType = {
    'Warranty Deed - Conventional':'WD',
    'Warranty Deed - Cash':'CWD',
    'Home just constructed and sold':'New',
    'Court Officer Deed/Estate':'COD',
    'Contract 15% Down payment regular terms':'Con',
    'Contract Low Down payment and low interest':'ConLw',
    'Contract Low Interest':'ConLI',
    'Contract Low Down':'ConLD',
    'Other':'Oth'
}
#%%
dict_SaleCondition = {
    'Normal Sale':'Normal',
    'Abnormal Sale -  trade, foreclosure, short sale':'Abnorml',
    'Adjoining Land Purchase':'AdjLand',
    'Allocation - two linked properties with separate deeds, typically condo with a garage unit':'Alloca',
    'Sale between family members':'Family',
    'Home was not completed when last assessed (associated with New Homes)':'Partial'
}