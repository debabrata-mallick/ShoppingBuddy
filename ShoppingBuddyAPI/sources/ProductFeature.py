import glob
import pandas as pd
import json
import os

WORD_MAPPINGS='ShoppingBuddyAPI/data/word_mappings/*' 
KEY_MAPPINGS='ShoppingBuddyAPI/data/key_mappings/*'
SUBKEY_MAPPINGS='ShoppingBuddyAPI/data/subkey_mappings/*'

class ProductFeature:
    '''
    A singleton class to generalize product features.
    Attributes:
        subkey_map: Dataframe
            Mapping of subkeys and keys
        word_mappings: Dataframe
            Mapping of words to subkeys
        key_mappings: Dataframe
            Properties of Key mappings
    Methods:
        getInstance()
            static method to return the sigleton instance of ProductFeature.
        mapProductFeatures(category,details,site)
            method to map feature list to generic features.
    '''

    __instance=None

    @staticmethod
    def getInstance():
        '''
        This is a static method to return the sigleton instance of ProductFeature.
        '''

        if ProductFeature.__instance == None:
            ProductFeature()
        return ProductFeature.__instance

    def getFolderContents(self,path,index):
        '''
        The method to get contents of a folder in a dataframe with the given index.
        '''
        dic = {}
        files=glob.glob(path)
        for filename in files:
            name=filename.split('\\')[-1].split('.')[0]
            content=pd.read_csv(filename)
            content.set_index(index)
            dic[name]=content
        return dic

    def __init__(self):
        '''
        The constructor of ProductFeature class.
        '''
        if ProductFeature.__instance == None:
            ProductFeature.__instance =self

            self.subkey_map = self.getFolderContents(SUBKEY_MAPPINGS, 'SubKey')
            self.key_mappings = self.getFolderContents(KEY_MAPPINGS, 'Key')
            self.word_mappings = self.getFolderContents(WORD_MAPPINGS, 'Word')
      
    def mapProductFeatures(self,category,details,site):
        '''
        The method to map the product features to generic features and perform necessary refactoring.
        Parameters:
            category:str
                category of the product
            details:Dictonary
                details or features of the product
            site:str
                Amazon or Flipkart
        '''
        mapped_features = {}
        unmapped_features = {}
        feature_list = []
        
        for k,v in details.items():  
            feature_word_mapping = self.word_mappings[category][(self.word_mappings[category].Word == k) & (self.word_mappings[category].Site == site)]
            
            if feature_word_mapping['Ignore'].values.size>0 and feature_word_mapping['Ignore'].values[0] == 'Y': # if its senseless / redundant feature, ignore it
                continue

            if feature_word_mapping['Keys'].values.size>0:
                key_for_feature = feature_word_mapping['Keys'].values[0]
                feature_key_mapping = self.key_mappings[category][(self.key_mappings[category].Key == key_for_feature)]
                feature_caption = feature_key_mapping['Caption'].values[0]
                delimiter = feature_key_mapping['Delimiter'].values[0]

                if key_for_feature is not None:
                    if feature_caption in mapped_features:
                        if delimiter == '\\n': #TODO improve logic
                            delimiter= os.linesep 
                        mapped_features[feature_caption] = mapped_features[feature_caption] + delimiter + v
                    else:
                        if feature_caption != feature_caption:
                            feature_caption=k
                        mapped_features[feature_caption] = v
                    feature_list.append(feature_caption)
            else:    
                #if key_for_feature is None:  # TODO delete? incorrect? 
                # TODO: try mapping by generalised approach
                #       if it still failes, to whats on next line
                unmapped_features[k] = v
                feature_list.append(k)

        mapped_features.update(unmapped_features)
        return mapped_features, feature_list #return single feature list
