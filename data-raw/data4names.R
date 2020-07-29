### Data for names package

pacman::p_load(tidyverse, fs)
pacman::p_load_gh("byuidss/DataPushR")

package_name_text <- "data4names"
base_folder <- "../../byuidatascience/"
user <- "byuidatascience"
package_path <- str_c(base_folder, package_name_text)
github_info <- dpr_info_github(user, package_name_text)
usethis::proj_set(package_path)

# github_info <- dpr_create_github(user, package_name_text)
# 
# package_path <- dpr_create_package(list_data = NULL,
#                                       package_name = package_name_text,
#                                       export_folder = base_folder,
#                                       git_remote = github_info$clone_url)
# usethis::proj_set(package_path)
##### dpr_delete_github(user, package_name_text) ########### End create section

names_year <- read_csv("projects/baby_names/derived_data/baby_names_state_year.csv") %>%
  select(-X1)

names_prob <- read_csv("projects/baby_names/derived_data/baby_names_gender_state.csv") %>%
  select(-X1)

usethis::use_data(names_year, names_prob)


dpr_export(names_year, export_folder = path(package_path, "data-raw"), 
           export_format = c(".csv", ".xlsx"))

dpr_export(names_prob, export_folder = path(package_path, "data-raw"), 
           export_format = c(".csv", ".xlsx", ".dta", ".json"))

dpr_document(names_year, extension = ".md.R", export_folder = usethis::proj_get(),
             object_name = "names_year", title = "Birth names counts by year for each US state",
             description = "A cleaned data set of birth names by year with counts for US states as well",
             source = "https://data.world/government/us-baby-names-by-state",
             var_details = list(name = "Baby name",
                                year = "Birth year",
                                AK = "Total for state",
                                Total = "Total for the US"))

dpr_document(names_prob, extension = ".md.R", export_folder = usethis::proj_get(),
             object_name = "names_prob", title = "Birth names gender",
             description = "A cleaned data set of birth names for gender and US states",
             source = "https://data.world/government/us-baby-names-by-state",
             var_details = list(name = "Baby name",
                                number_female = "Number of females",
                                number_male = "Number of males",
                                prob_female = "Probability the name is female",
                                prob_male = "Probability the name is male",
                                AK = "Total for state"))


dpr_readme(usethis::proj_get(), package_name_text, user)

dpr_write_script(folder_dir = package_path, r_read = "scripts_general/names_package.R", 
                 r_folder_write = "data-raw", r_write = str_c(package_name_text, ".R"))

dpr_write_script(folder_dir = package_path, r_read = "projects/baby_names/data_format.py", r_folder_write = "data-raw",
                 r_write = "names.py")

devtools::document(package_path)

dpr_push(folder_dir = package_path, message = "'First data set'", repo_url = NULL)
