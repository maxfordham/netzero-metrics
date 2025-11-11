
# Buildings

|   TargetYear | Name   |
|-------------:|:-------|
|         2025 | A      |
|         2030 | B      |
|         2025 | C      |

# Areas

|   GrossInternalArea | BuildingType                          | ConstructionMethod   | BuildingName   |
|--------------------:|:--------------------------------------|:---------------------------|:---------------|
|                  10 | Office - General                      | newbuild                   | A              |
|                  10 | Office - General                      | retrofit-in-one-go         | A              |
|                  20 | Commercial Resi - Student Residential | newbuild                   | B              |
|                  20 | Commercial Resi - Student Residential | retrofit-in-one-go         | B              |
|                  20 | Commercial Resi - Student Residential | retrofit-in-one-go         | B              |

# Areas with Year

| BuildingName   |   GrossInternalArea | BuildingType                          | ConstructionMethod   |   TargetYear |
|:---------------|--------------------:|:--------------------------------------|:---------------------------|-------------:|
| A              |                  10 | Office - General                      | newbuild                   |         2025 |
| A              |                  10 | Office - General                      | retrofit-in-one-go         |         2025 |
| B              |                  20 | Commercial Resi - Student Residential | newbuild                   |         2030 |
| B              |                  20 | Commercial Resi - Student Residential | retrofit-in-one-go         |         2030 |
| B              |                  20 | Commercial Resi - Student Residential | retrofit-in-one-go         |         2030 |

# Custom Energy Use Intensities

| BuildingType                          |   Target | Description             | TargetName   | ConstructionMethod   |
|:--------------------------------------|---------:|:------------------------|:-------------|:---------------------------|
| Office - General                      |       70 | better than NZC target! | ambitious!   | newbuild                   |
| Office - General                      |       70 | better than NZC target! | ambitious!   | retrofit-in-one-go         |
| Commercial Resi - Student Residential |       70 | better than NZC target! | ambitious!   | newbuild                   |
| Commercial Resi - Student Residential |       70 | better than NZC target! | ambitious!   | retrofit-in-one-go         |

# UKNZCB Energy Use Intensities

|   Year | BuildingType                          |   Target | BuildingTypeShorthand   | Unit         | ConstructionMethod   |
|-------:|:--------------------------------------|---------:|:------------------------|:-------------|:---------------------------|
|   2025 | Commercial Resi - Student Residential |       75 | Stud. Resi.             | kWh/m²GIA/yr | newbuild                   |
|   2030 | Commercial Resi - Student Residential |       67 | Stud. Resi.             | kWh/m²GIA/yr | newbuild                   |
|   2025 | Office - General                      |       85 | Off. Gen. (GIA)         | kWh/m²GIA/yr | newbuild                   |
|   2030 | Office - General                      |       72 | Off. Gen. (GIA)         | kWh/m²GIA/yr | newbuild                   |
|   2025 | Commercial Resi - Student Residential |      110 | Stud. Resi.             | kWh/m²GIA/yr | retrofit-in-one-go         |
|   2030 | Commercial Resi - Student Residential |       99 | Stud. Resi.             | kWh/m²GIA/yr | retrofit-in-one-go         |
|   2025 | Office - General                      |      100 | Off. Gen. (GIA)         | kWh/m²GIA/yr | retrofit-in-one-go         |
|   2030 | Office - General                      |       85 | Off. Gen. (GIA)         | kWh/m²GIA/yr | retrofit-in-one-go         |

