import math
import pickle
import numpy                as np
import pandas               as pd
import datetime
import inflection


class Rossmann ( object ):
    def __init__ (self):
        self.home_path = ''

        self.competition_distance_scaler    = pickle.load( open( self.home_path + 'feature/competition_distance_scaler.pk1', 'rb' ) )
        self.competition_time_month_scaler  = pickle.load( open( self.home_path + 'feature/competition_time_month_scaler.pk1', 'rb' ) )
        self.promo_time_week_scaler         = pickle.load( open( self.home_path + 'feature/promo_time_week_scaler.pk1', 'rb' ) )
        self.year_scaler                    = pickle.load( open( self.home_path + 'feature/year_scaler.pk1', 'rb' ) )
        self.store_type_scaler              = pickle.load( open( self.home_path + 'feature/store_type_scaler.pk1', 'rb' ))

    
    def data_clenning (self, df1):
        
        ## 1.1. Rename Columns
        df1 = df1.drop(columns = ['Customers'], axis=1)

        cols_old = ['Store', 'DayOfWeek', 'Date', 'Sales', 'Open', 'Promo', 'StateHoliday', 'SchoolHoliday',
                    'StoreType', 'Assortment','CompetitionDistance', 'CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear',
                    'Promo2', 'Promo2SinceWeek', 'Promo2SinceYear', 'PromoInterval']

        snakecase = lambda x : inflection.underscore( x )

        cols_new = list( map( snakecase, cols_old) )

        #rename
        df1.columns = cols_new


        ## 1.3. Data Types
        df1['date'] = pd.to_datetime( df1['date'] )

        ## 1.5. Fillout NA
        df1['competition_distance'] = df1['competition_distance'].apply(lambda x : 2000000.0 if math.isnan( x ) else x)

        # competition_open_since_month
        df1['competition_open_since_month'] = df1.apply(lambda x : x['date'].month
                                                        if math.isnan( x['competition_open_since_month'] )
                                                        else x['competition_open_since_month'],
                                                        axis = 1)

        # competition_open_since_year
        df1['competition_open_since_year'] = df1.apply(lambda x : x['date'].year
                                                        if math.isnan( x['competition_open_since_year'] )
                                                        else x['competition_open_since_year'],
                                                        axis = 1)

        # promo2_since_week
        df1['promo2_since_week'] = df1.apply(lambda x : x['date'].week
                                                        if math.isnan( x['promo2_since_week'] )
                                                        else x['promo2_since_week'],
                                                        axis = 1)

        # promo2_since_year
        df1['promo2_since_year'] = df1.apply(lambda x : x['date'].year
                                                        if math.isnan( x['promo2_since_year'] )
                                                        else x['promo2_since_year'],
                                                        axis = 1)

        # promo_interval
        month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sept', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

        df1['promo_interval'].fillna(0, inplace=True ) # preenchimento do NA com 0 para facilitar a compraração

        df1['month_map'] = df1['date'].dt.month.map( month_map ) # Extração do mês da 'data' 

        df1['is_promo'] = df1[['promo_interval', 'month_map']].apply(lambda x: 0 if x['promo_interval'] == 0 else
                                                                                1 if x['month_map'] in x['promo_interval'].split(',') else 0,
                                                                                axis = 1)

        ## 1.6. Change types
        df1['competition_open_since_month'] = df1['competition_open_since_month'].astype( 'int64' )
        df1['competition_open_since_year'] = df1['competition_open_since_year'].astype( 'int64' )

        df1['promo2_since_week'] = df1['promo2_since_week'].astype( 'int64' )
        df1['promo2_since_year'] = df1['promo2_since_year'].astype( 'int64' )
        
        return df1

    def feature_engineering (self, df2):
        
        ## 2.4. Feature Engineering
        # year
        df2['year'] = df2['date'].dt.year
        # month
        df2['month'] = df2['date'].dt.month
        # day
        df2['day'] = df2['date'].dt.day
        # week of year
        df2['week_of_year'] = df2['date'].dt.isocalendar().week
        # year week
        df2['year_week'] = df2['date'].dt.strftime('%Y-%W')
        
        # competition since - quanto tempo da data da compra desde quando a competição começou
        df2['competition_since'] = df2.apply(lambda x: datetime.datetime( year=x['competition_open_since_year'], month=x['competition_open_since_month'], day=1), axis=1)
        
        df2['competition_time_month'] = ((df2['date'] - df2['competition_since']) / 30).apply(lambda x: x.days).astype('int64')
        
        # promo since
        
        df2['promo_since'] = df2['promo2_since_year'].astype('str') + '-' + df2['promo2_since_week'].astype('str')
        
        df2['promo_since'] = df2['promo_since'].apply( lambda x: datetime.datetime.strptime( x +'-1', '%Y-%W-%w') - datetime.timedelta(days=7) )
        df2['promo_time_week'] = ((df2['date'] - df2['promo_since']) /7).apply( lambda x: x.days).astype('int64')
        
        # assortment
        df2['assortment'] = df2['assortment'].apply(lambda x: 'basic' if x == 'a'
                                                    else'extra' if x == 'b'
                                                    else 'extended')
        
        # state hollyday
        df2['state_holiday'] = df2['state_holiday'].apply(  lambda x: 'public_holiday' if x == 'a'
                                                            else 'easter_holiday' if x == 'b'
                                                            else 'christmas' if x == 'c'
                                                            else 'regular_day')
        # 3.0 FILTRAGEM DAS VARIÁVEIS
        
        ## 3.1. Filtragem das Linhas
        df2 = df2[(df2['open'] != 0)]
        
        ## 3.2. Seleção das Colunas
        cols_drop = ['open', 'promo_interval', 'month_map']
        df2 = df2.drop(cols_drop, axis=1)
        
        return df2
    
