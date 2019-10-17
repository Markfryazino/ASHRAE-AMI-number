import unittest
import numpy as np
import pandas as pd

def fillna_by_time(site_id_data, column):
    # If we know that column is sorted by the time,
    # for every NaN value we can use the last non-Nan value
    # which was met before

    # We should have a first value not to be NaN
    # to fill others
    site_id_data = site_id_data.copy()
    if np.isnan(site_id_data[column][0]):
        for i in site_id_data[column]:
            if not np.isnan(i):
                site_id_data.loc[site_id_data.index == 0, column] = i
                break
                
        assert np.isnan(site_id_data[column][0]) == False

    # Now we start with index 1
    # We fill column in such a way that any value has
    # non-NaN value on previous index
    for i in range(1, len(site_id_data)):
        if np.isnan(site_id_data[column][i]):
            site_id_data.loc[site_id_data.index == i, column] = site_id_data[column][i - 1]
    
    return site_id_data

# General unittests
class Check_fillna_by_time(unittest.TestCase): 
    test = pd.DataFrame(
            {'clmn1':[np.NaN,np.NaN,np.NaN], 'clmn2':[np.NaN, 1, np.NaN],'clmn3':[1, np.NaN, 2]}
        )
    def test_zero_el_isnt_nan(self):
        answer = pd.DataFrame(
            {'clmn1':[np.NaN,np.NaN,np.NaN], 'clmn2':[np.NaN, 1, np.NaN],'clmn3':[1, 1, 2]}
        )
        self.assertFalse((fillna_by_time(self.test, 'clmn3')['clmn3'] - answer['clmn3']).any())
        
    def test_zero_el_is_nan_without_assert(self):
        answer = pd.DataFrame(
            {'clmn1':[np.NaN,np.NaN,np.NaN], 'clmn2':[1, 1, 1],'clmn3':[1, np.NaN, 2]}
        )
        self.assertFalse((fillna_by_time(self.test, 'clmn2')['clmn2'] - answer['clmn2']).any())
        
    def test_zero_el_is_nan_with_assert(self):
        # crutch!!!
        try:
            fillna_by_time(self.test, 'clmn1')
        except AssertionError:
            self.assertEqual(True, True)
        else:
            self.assertEqual(False, True)
