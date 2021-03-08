#!/usr/bin/env python
#
#
#
import re
import datetime
from db_related import TableAware, LookupDB, SQConnect
from decimal import Decimal, ROUND_HALF_UP, ROUND_UP, ROUND_05UP


class RetailOps(object):
    """Collection of Retail Operations."""

    def __init__(self, debug=False):
        """Amalgamation of all the retail number calculations.
        Decimal Unit refers to '1.00', '10.00', '0.00', etc.
        """

    def DoMargin(self, avgcost, calcMargin, unitd):
        """Calculate Margin (AvgCost * (Decimal(Margin) / 100)."""
        profit_margin = Decimal(calcMargin) / 100
        newRetail = (Decimal(avgcost) / (profit_margin) * Decimal(unitd))
        return newRetail


    def GetMargin(self,avgcost, retail, unitd):
        """Get Margin from an already calculated Retail.
        Requires AvgCost, Retail, Decimal Unit i.e. '1.00'. 
        """    
        raw = (Decimal(retail) / Decimal(unitd))
        new = ((Decimal(raw) - Decimal(avgcost)) / Decimal(raw)) * 100
        return new

    def MarginUpdate(self, avg_cost, retail, unit):
        """Re-adjust Margin in margin Column according to avg_cost."""
        actual_retail = Decimal(retail)/Decimal(unit)
        gross_profit = Decimal(actual_retail) - Decimal(avg_cost)
        deci_margin = Decimal(gross_profit) / Decimal(actual_retail)
        perc_margin = Decimal(deci_margin) * Decimal(100)
        percentage_margin = self.DoRound(perc_margin, '1.000')
        return percentage_margin


    def RoundNickel(self, x):
        """Round to the nearest Nickel."""    
        a = .05
        b = round(Decimal(x) / Decimal(a))
        c = Decimal(b) * Decimal(a)
        return c


    def DoRound(self, oldmoney, unitd='1.00', typd='plain'):
        """Round Sums using different definable schemes."""
        noPenny, rndScheme = False, '3'
        if typd == 'tax':
            (noPenny, rndScheme) = LookupDB('tax_tables').Specific('TAX','tax_name','no_pennies_rounding, RNDscheme')
        
        roundtype = {'1':'ROUND_DOWN','2':'ROUND_HALF_UP','3':'ROUND_UP'}
        if rndScheme == 0:
            rndScheme = 3
        
        rnd = str(rndScheme)
        newMoney = Decimal(Decimal(oldmoney).quantize(Decimal(unitd), rounding=roundtype[rnd]))
        return newMoney

    def DoDiscount(self, retail, discount):
        """Return New Retail after Applying Discount."""
        newRetail = Decimal(retail) - (Decimal(retail) * (Decimal(discount) / 100))
        return newRetail

    def CheckDiscount(self, itemNumber=None, custNum=None, on_discount=None):
        query = 'SELECT do_not_discount FROM item_detailed2 WHERE upc=(?)'
        data = (itemNumber,)
        nodiscount = SQConnect(query, data).ONE()
        discount = 0
        dnd = False
        if nodiscount is None or nodiscount[0] is True or nodiscount[0] == 1:
            dnd = True

        if len(custNum) > 0:
            query = '''SELECT fixed_discount, discount_amt
                    FROM customer_sales_options
                    WHERE cust_num=(?)'''
            data = (custNum,)
            returnd = SQConnect(query, data).ONE()
            
            (fixed_discount, discount_amt) = returnd
            if returnd is not None:
                if returnd[0] is True or returnd[0] == 1:
                    discount = returnd[1]
                
        discountSingle = wx.FindWindowByName('pos_discounttype_combobox').GetValue()
        if discountSingle == 'Discount All':
            discountAll = wx.FindWindowByName('pos_discountpercent_txtctrl').GetCtrl()
            if discountAll and discountAll > 0:
                discount = discountAll
    
        if on_discount > 0:
            discount = on_discount
        
        if dnd is True:
            discount = 0
        
        return discount


    def LevelDiscount(self, upc, qty, discount, totalprice):
        qtyd = int(qty)
        retails = self.RetailSifting(upc)
        startret = Decimal(retails['standard_price']['price'])*Decimal(qtyd)
        #pout.v(f'Discount @ LevelDiscount : {discount}')
        discprice = startret
        if re.match('[0-9]', str(discount), re.I):
            discprice = self.DoDiscount(startret, discount)
            
        levelprice = startret
        lvl = ''
        
        if qtyd > 1:
            for level in retails:
                if 'standard' in level:
                    continue
                #pout.v(f'Level : {level}')
                #pout.v(f'Retails[{level}] : {retails[level]}')
                if retails[level]['price'] > 0:
                    lastnum = int(retails[level]['unit'])
                    
                    if qtyd >= lastnum:
                        levelprice = retails[level]['price']
                        lvl = level
        
        RetPrice = (levelprice, self.levelLabel(lvl))                
        if Decimal(discprice) < Decimal(levelprice):
            RetPrice = (self.DoRound(discprice), f"{discount}%")

        if totalprice > Decimal(RetPrice[0]):
            totalprice = RetPrice[0]
            disccol = RetPrice[1]

        return RetPrice 
        

    def levelLabel(self, label):
        c = label
        if 'level' in label:
            a = re.search('level_(.)_price', label, re.IGNORECASE)
            b = a.group(1)
            c = b.upper()

        return c

    def Dollars(self, amount):
        if amount >= 0:
            return '{:,.2f}'.format(amount)
        else:
            return '{:,.2f}'.format(-amount)


    # def StartingMargin(self, name):
    #     grid = wx.FindWindowByName('inv_details_cost_grid')
    #     current_margin = GridOps(grid.GetName()).GetCell('Margin %',0)
    #     if float(current_margin) > 10:
    #         StartingMargin_L = current_margin
    #         item = wx.FindWindowByName('details_startingMargin_numctrl').GetCtrl()
    #         wx.FindWindowByName('details_startingMargin_numctrl').GetCtrl(current_margin)
    #     else:
    #         StartingMargin_L = '50'
        
    #     return StartingMargin_L

    def RetailSifting(self, upc):
        sift_list = [(0, 'item_retails', 'standard_unit', 'standard_price'),
                    (1,'item_retails', 'level_a_unit', 'level_a_price'), 
                    (2, 'item_retails', 'level_b_unit', 'level_b_price'),
                    (3, 'item_retails', 'level_c_unit', 'level_c_price'),
                    (4, 'item_retails', 'level_d_unit', 'level_d_price'),
                    (5, 'item_retails', 'level_e_unit', 'level_e_price'),
                    (6, 'item_retails', 'level_f_unit', 'level_f_price'),
                    (7, 'item_retails', 'level_g_unit', 'level_g_price'),
                    (8, 'item_retails', 'level_h_unit', 'level_h_price'),
                    (9, 'item_retails', 'level_i_unit', 'level_i_price'),
                    (10, 'item_retails', 'compare_unit', 'compare_price'),
                    (11, 'item_retails', 'on_sale_unit', 'on_sale_price')]
        sift_dict = {}
        retail = '1'
        for row, table, unit_field, price_field in sift_list:
            query = '''SELECT {}, {}
                    FROM {}
                    WHERE upc=(?)'''.format(unit_field, price_field, table)
                        
            data = (str(upc).upper().strip(),)
            returnd = SQConnect(query,data).ONE()
            
            if not returnd:
                return None
                
            unitd, retaild = returnd
            sift_dict[price_field] = {'unit':str(unitd), 'price': retaild}
                           
        return sift_dict    

    # def GetRetail(upcd, cust_num, retailsd_JSON=None, on_discount=None, debug=False):
    #     if retailsd_JSON is None:
    #         discountd = None
    #         new_retail = '0'
        
    #     else:   
    #         retailsd = retailsd_JSON
    #         retail_regular = retailsd['standard_price']['price']
    #         if on_discount[1] > 0:
    #             discount = CheckDiscount(upcd, cust_num, on_discount[1])
    #         else:
    #             discount = CheckDiscount(upcd, cust_num, on_discount[0])
            
    #         if discount > 0:
    #             discountd = str(discount)
    #             new_retail = DiscountIt(retail_regular, discountd)
    #         else:
    #             discountd = None
    #             new_retail = retail_regular
                                
        
    #     return discountd,new_retail
    
    
    def GetTaxRate(price):
        fields = '''min_sale, max_sale, from_amt0, 
                    tax_rate0, from_amt1, tax_rate1, from_amt2, tax_rate2''' 
        returnd = LookupDB('tax_tables').Specific('TAX','tax_name',fields)
        (min_sale, max_sale, from_amt0, tax_rate0, from_amt1,
        tax_rate1, from_amt2, tax_rate2) = returnd 
        if returnd is None:
            return
        
        if Decimal(price) > Decimal(min_sale):
            if Decimal(price) > Decimal(from_amt0):
                taxd = Decimal(tax_rate0)    

            if Decimal(from_amt1) > 0:
                if Decimal(price) > Decimal(from_amt1):
                    taxd = Decimal(tax_rate1)

            if Decimal(from_amt2) > 0:
                if Decimal(price) > Decimal(from_amt2):
                    taxd = Decimal(tax_rate2)

        if taxd >= 1:
            taxd = Decimal(taxd) / 100
        
        return taxd
    

    # def GetTaxable(upc, taxable, discount_col=''):
    #     Taxed = True
    #     query = 'SELECT tax1,tax2,tax3,tax4,tax_never FROM item_detailed2 WHERE upc=(?)'
    #     data = (upc,)
    #     returnd = SQConnect(query, data).ONE()
    #     tax1, tax2, tax3, tax4, tax_never = 0,0,0,0,0
    #     if returnd is not None:
    #         (tax1,tax2,tax3,tax4,tax_never) = returnd
        
    #     tax_list = [(0, tax1),('A',tax2),('B',tax3),('C',tax4)]
    #     tx_dict = {}
    #     for key, value in tax_list:
    #         tx_dict[key] = value
        
    #     if discount_col == '' or discount_col is None:
    #         discount_col = 0
        
    #     if tx_dict[discount_col] == 1 or tx_dict is True:
    #         Taxed = False
        
    #     if taxable is False:
    #         Taxed = False
            
    #     if tax_never == 1:
    #         Taxed = False
        
    #     if Taxed is False:
    #         pr_tax = 'nTx'
    #     else:   
    #         pr_tax = 'Tx'
        
    #     return Taxed,pr_tax

    def CheckTaxHoliday(upc):
        """Check Tax Holiday Worksheet."""
        query = 'SELECT begin_date, end_date, upc, active FROM tax_holiday'
        data = ''
        returnd = SQConnect(query, data).ALL()
        taxexempt = False
        for begins, ends, upcs, active in returnd:
            if active == 1:
                begin = datetime.date(begins)
                end = datetime.date(ends)
                today = datetime.datetime.today()
                if begin < today < end:
                    if upc in upcs:
                        taxexempt = True

        return taxexempt
