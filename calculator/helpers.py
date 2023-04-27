from scipy import stats
import pandas as pd
import numpy
from typing import Tuple
import random

class TestStatistiques:

    def __init__(self) -> None:
        pass

    @staticmethod
    def t_test_independant(
            variable_1: numpy.ndarray,
            variable_2: numpy.ndarray
        ) -> Tuple[float, float]:
        stat_value, p_value = stats.ttest_ind(
            variable_1,
            variable_2
        )
        return stat_value, p_value

    @staticmethod
    def mann_and_whitney_test(
            variable_1: numpy.ndarray,
            variable_2: numpy.ndarray
        ) -> Tuple[float, float]:
        stat_value, p_value = stats.mannwhitneyu(
            variable_1,
            variable_2
        )
        return stat_value, p_value
    
    @staticmethod
    def normality_test(variable) -> Tuple[float, float]:
        stat_value, p_value = stats.shapiro(variable)
        return stat_value, p_value

    @staticmethod
    def anova(*sample) -> Tuple[float, float]:
        stat_value, p_value = stats.f_oneway(*sample)
        return stat_value, p_value

    @staticmethod
    def kruskal_wallis(*sample) -> Tuple[float, float]:
        stat_value, p_value = stats.kruskal(*sample)
        return stat_value, p_value
    @staticmethod
    def post_hoc_tukey(*sample):
        tukey_instance = stats.tukey_hsd(*sample)
        return tukey_instance

    @staticmethod
    def t_test_apparie(variable_1, variable_2, raise_error: bool = False) -> Tuple[float, float]:
        if raise_error:
            if len(variable1) != len(variable_2):
                raise ValueError("Les longeurs des echantillons doivent être identiques")
        else:
            stat_value, p_value = stats.ttest_rel(variable1, variable_2)
            return stat_value, p_value

    @staticmethod
    def wilcoxon_apparai_rang_signe(variable_1, variable_2, raise_error: bool = False) -> Tuple[float, float]:
        if raise_error:
            if len(variable1) != len(variable_2):
                raise ValueError("Les longeurs des echantillons doivent être identiques")
        else:
            stat_value, p_value = stats.wilcoxon(variable1, variable_2)
            return stat_value, p_value


class ProcessStatistique(TestStatistiques):

    def __init__(self, data) -> None:
        super().__init__()
        self.data = data
        quali, quanti, clean = self.process_typing_data()
        self.cleaning_data = clean
        self.var_quali = quali
        self.var_quanti = quanti
        self._choice_quali = None
        self._choice_quanti = None
        self._post_hoc = None

    @property
    def choice_quali(self):
        return self._choice_quali

    @choice_quali.setter
    def choice_quali(self, value):
        self._choice_quali = value

    @property
    def choice_quanti(self):
        return self._choice_quanti

    @choice_quanti.setter
    def choice_quanti(self, value):
        self._choice_quanti = value

    @property
    def apply_posthoc(self):
        return self._post_hoc

    @apply_posthoc.setter
    def apply_posthoc(self, value):
        self._post_hoc = value
    
    @staticmethod
    def create_dict_from_df(df) -> dict:
        dict_data = df.to_dict(orient='records')
        return dict_data

    @staticmethod
    def change_comma_to_point(df: pd.DataFrame) -> pd.DataFrame:
        for i in df.columns:
            for idx, j in enumerate(df[i]):
                try:
                    new = j.replace(',', '.')
                    df[i][idx] = new
                except:
                    pass
        return df

    @staticmethod
    def change_type(df: pd.DataFrame) -> pd.DataFrame:
        for i in df.columns:
            if isinstance(df[i].dtype, object):
                try:
                    df[i] = df[i].astype(float)
                except:
                    pass
        new = df.copy()
        return new

    @staticmethod
    def liste_variable(df: pd.DataFrame) -> Tuple[list, list]:
        quali = []
        quanti = []
        for i in df.columns:
            if isinstance(df[i][0], str):
                quali.append(i)
            else:
                quanti.append(i)
        return quali, quanti

    @staticmethod
    def special_transform_index_match(df: pd.DataFrame) -> pd.DataFrame:
        df['Match'] = df['Match'].astype(str)
        new = df.copy()
        return new

    @staticmethod
    def is_significatif(value):
        if value <= 0.05:
            return True
        else:
            return False

    def get_number_variables_qualitative(self) -> int:
        return len(self.var_quali)

    def get_number_variables_quantitative(self) -> int:
        return len(self.var_quanti)

    def random_choice_variables(self) -> Tuple:
        choice_quali = random.sample(population=self.var_quali, k=1)
        choice_quanti = random.sample(population=self.var_quanti, k=1)
        return choice_quali, choice_quanti

    def get_number_modalite_qualitative(self, colonne) -> int:
        return len(self.cleaning_data[colonne].unique())

    def get_all_number_value_for_test_decision(self):
        choice_quali, choice_quanti = self.random_choice_variables()
        number_modalite = self.get_number_modalite_qualitative(choice_quali[0])
        number_quali = len(choice_quali)
        number_quanti = len(choice_quanti)
        return choice_quali, choice_quanti, number_modalite, number_quali, number_quanti

    def create_dataframe_from_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.data, sep=';')
        return df

    def process_typing_data(self) -> Tuple[list, list, pd.DataFrame]:
        create = self.create_dataframe_from_data()
        new = self.change_comma_to_point(create)
        step_1 = self.change_type(new)
        step_2 = self.special_transform_index_match(step_1)
        quali, quanti = self.liste_variable(step_2)
        return quali, quanti, step_2

    def is_normality(self, variable) -> Tuple:
        _, value = self.normality_test(variable)
        if value <= 0.05:
            return False, value
        else:
            return True, value

    def filter_groupe_by_modalite_for_test(self, features: list, quanti) -> list:
        data = []
        modalites = self.cleaning_data[features[0]].unique()
        for modalite in modalites:
            filter_groupe = self.cleaning_data[self.cleaning_data[features[0]] == modalite]
            data.append(filter_groupe[quanti[0]])
        return data

    def choice_test(self, choice_quali, choice_quanti, number_modalite, number_quali, number_quanti):
        _, pvalue, normality, test_type, test_name = [None] * 5
        self.choice_quali = choice_quali
        self.choice_quanti = choice_quanti
        if number_quali == 1 and number_quanti == 1:
            if number_modalite == 2:
                is_normal, normality = self.is_normality(self.cleaning_data[choice_quanti[0]])
                data = self.filter_groupe_by_modalite_for_test(choice_quali, choice_quanti)
                if is_normal:
                    _, pvalue = self.t_test_independant(
                        variable_1=data[0],
                        variable_2=data[1]
                    )
                    test_type, test_name = "Test parametrique", "T-test de student"
                else:
                    _, pvalue = self.mann_and_whitney_test(
                        variable_1=data[0],
                        variable_2=data[1]
                    )
                    test_type, test_name = "Test non-parametrique", "Test de Mann Whitney"
            elif number_modalite >= 3:
                data = self.filter_groupe_by_modalite_for_test(choice_quali, choice_quanti)
                check_bool = []
                for i in choice_quanti:
                    is_normal, normality = self.is_normality(self.cleaning_data[i])
                    if is_normal:
                        check_bool.append(True)
                    else:
                        check_bool.append(False)
                if all(check_bool):
                    _, pvalue = self.anova(*data)
                    test_type, test_name = "Test parametrique", "ANOVA"
                    if self.is_significatif(pvalue):
                        post_hoc = self.post_hoc_tukey(*data)
                        self.apply_posthoc = post_hoc
                else:
                    _, pvalue = self.kruskal_wallis(*data)
                    test_type, test_name = "Test non-parametrique", "Kruskal Wallis"
                    if self.is_significatif(pvalue):
                        post_hoc = self.post_hoc_tukey(*data)
                        self.apply_posthoc = post_hoc
        elif number_quali == 2 and number_quanti == 0:
            _, pvalue = "TEST", "CHI2 SQUARE"
            test_type, test_name = "Test de frequence", "Chi Square"
        elif number_quali == 0 and number_quanti == 2:
            data = self.filter_groupe_by_modalite_for_test(choice_quali, choice_quanti)
            check_bool = []
            for i in choice_quanti:
                is_normal, normality = self.is_normality(self.cleaning_data[i])
                if is_normal:
                    check_bool.append(True)
                else:
                    check_bool.append(False)
            if all(check_bool):
                _, pvalue = self.t_test_apparie(
                    variable_1=data[0],
                    variable_2=data[1],
                    raise_error=True
                )
                test_type, test_name = "Test parametrique", "T-test apparie"
            else:
                _, pvalue = self.wilcoxon_apparai_rang_signe(
                    variable_1=data[0],
                    variable_2=data[1],
                    raise_error=True
                )
                test_type, test_name = "Test non-parametrique", "Wilcoxon rang signe"
        return pvalue, normality, test_type, test_name

    def __str__(self):
        if self._post_hoc is None:
            return f"Le test sur les variables {self._choice_quali} et {self._choice_quanti} a ete effectue avec succes"
        else:
            return f"Le test sur les variables {self._choice_quali} et {self._choice_quanti} a ete effectue avec succes. Les tests post_hoc presentent les resultat suivant: {self._post_hoc}"
