import time
from datetime import datetime
import Global_var
from Insert_On_Datbase import insert_in_Local
import sys , os
import string
import time
from datetime import datetime
import html
import re
import wx
app = wx.App()

def remove_html_tag(string):
    cleanr = re.compile('<.*?>')
    main_string = re.sub(cleanr, '', string)
    return main_string

def scrap_data(browser,get_htmlsource,tender_link):

    SegField = []
    for data in range(45):
        SegField.append('')
    
    a = True
    while a == True:
        try:
            Contact_name = ''
            Region = ''
            for Contact_name in browser.find_elements_by_xpath('//*[@id="contactPersonspan"]'):
                Contact_name = Contact_name.get_attribute('innerText')
                Contact_name = string.capwords(str(Contact_name))
                break
            for Region in browser.find_elements_by_xpath('//*[@id="div_region"]'):
                Region = Region.get_attribute('innerText').strip()
                Region = string.capwords(str(Region))
                break

            SegField[2] = f'{Contact_name}<br>\n{Region} , Malaysia'
            
            Purchaser = get_htmlsource.partition('Buyer:')[2].partition("</td>")[0].strip()
            if Purchaser != '':
                Purchaser = remove_html_tag(Purchaser)
                if Purchaser == 'MIROS':
                     Purchaser = 'Malaysian Institute of Road Safety Research (MIROS)'
                elif Purchaser == 'KESEDAR':
                    Purchaser = 'SOUTH KELANTAN DEVELOPMENT BOARD (KESEDAR)'
                elif Purchaser == 'LHDNM':
                    Purchaser = 'Inland Revenue Board of Malaysia (LHDNM)'
                elif Purchaser == 'SKM':
                    Purchaser = 'SuruhanJaya Koperasi Malaysia (SKM)'
                elif Purchaser == 'UTHM':
                    Purchaser = 'Universiti Tun Hussein Onn Malaysia (UTHM)'
                elif Purchaser == 'LKIM':
                    Purchaser = 'Malaysian Fisheries Development Authority (LKIM)'
                elif Purchaser == 'KEDA':
                    Purchaser = 'Kedah Regional Development Authority (KEDA)'
                elif Purchaser == 'RAC':
                    Purchaser = 'Railway Assets Corporation (RAC)'
                else:
                    SegField[12] = Purchaser.strip().upper()
                SegField[12] = Purchaser.strip().upper()

            for Tender_id in browser.find_elements_by_xpath('//*[@id="tenderNumberspan"]'):
                Tender_id = Tender_id.get_attribute('innerText')
                SegField[13] = Tender_id.strip()
                break

            for Title in browser.find_elements_by_xpath('//*[@id="descOfWorkspan"]'):
                Title = Title.get_attribute('innerText')
                Title = string.capwords(str(Title))
                SegField[19] = Title.strip()
                break

            for Tender_deadline in browser.find_elements_by_xpath('//*[@id="receiptOfTendToDatespan"]'):
                Tender_deadline = Tender_deadline.get_attribute('innerText').strip()
                datetime_object = datetime.strptime(Tender_deadline, '%d-%m-%Y %H:%M')
                Tender_Deadline = datetime_object.strftime("%Y-%m-%d")
                SegField[24] = Tender_Deadline
                break

            SegField[28] =  tender_link

            vendor_Category = ''
            tender_Remark = ''
            tender_Type = ''
            Multiple_Submission = ''
            currency = ''
            tenderStage = ''
            for vendor_Category in browser.find_elements_by_xpath('//*[@id="vendorCategoryspan"]'):
                vendor_Category = vendor_Category.get_attribute('innerText').strip()
                vendor_Category = string.capwords(str(vendor_Category))
                break
            for tender_Remark in browser.find_elements_by_xpath('//*[@id="tendRemarkspan"]'):
                tender_Remark = tender_Remark.get_attribute('innerText').strip()
                tender_Remark = string.capwords(str(tender_Remark))
                break
            for tender_Type in browser.find_elements_by_xpath('//*[@id="tenderTypespan"]'):
                tender_Type = tender_Type.get_attribute('innerText').strip()
                tender_Type = string.capwords(str(tender_Type))
                break
            for Multiple_Submission in browser.find_elements_by_xpath('//*[@id="isMultipleSubmissionspan"]'):
                Multiple_Submission = Multiple_Submission.get_attribute('innerText').strip()
                Multiple_Submission = string.capwords(str(Multiple_Submission))
                break
            for currency in browser.find_elements_by_xpath('//*[@id="currencyspan"]'):
                currency = currency.get_attribute('innerText').strip()
                currency = string.capwords(str(currency))
                break
            for tenderStage in browser.find_elements_by_xpath('//*[@id="tenderStagespan"]'):
                tenderStage = tenderStage.get_attribute('innerText').strip()
                tenderStage = string.capwords(str(tenderStage))
                break


            SegField[18] = f'{SegField[19]}<br>\nVendor Category: {vendor_Category}<br>\nTender Remark: {tender_Remark}<br>\nTender Type: {tender_Type}<br>\nCurrency: {currency}<br>\ntender Stage: {tenderStage}'
            
            
            SegField[14] = '2'
            SegField[22] = "0"
            SegField[26] = "0.0"
            SegField[27] = "0"  # Financier
            SegField[7] = 'MY'
            SegField[31] = 'tenderwizard.my'
            SegField[20] = ""
            SegField[21] = "" 
            SegField[42] = SegField[7]
            SegField[43] = "" 

            for SegIndex in range(len(SegField)):
                print(SegIndex, end=' ')
                print(SegField[SegIndex])
                SegField[SegIndex] = html.unescape(str(SegField[SegIndex]))
                SegField[SegIndex] = str(SegField[SegIndex]).replace("'", "''")

            if len(SegField[19]) >= 200:
                SegField[19] = str(SegField[19])[:200]+'...'

            if len(SegField[18]) >= 1500:
                SegField[18] = str(SegField[18])[:1500]+'...'

            if SegField[19] == '':
                wx.MessageBox(' Short Desc Blank ','tenderwizard.my', wx.OK | wx.ICON_INFORMATION)
            else:
                check_date(get_htmlsource, SegField)
                pass
            
            a = False
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                  exc_tb.tb_lineno)
            a = True
            time.sleep(5)


def check_date(get_htmlSource, SegField):
    deadline = str(SegField[24])
    curdate = datetime.now()
    curdate_str = curdate.strftime("%Y-%m-%d")
    try:
        if deadline != '':
            datetime_object_deadline = datetime.strptime(deadline, '%Y-%m-%d')
            datetime_object_curdate = datetime.strptime(curdate_str, '%Y-%m-%d')
            timedelta_obj = datetime_object_deadline - datetime_object_curdate
            day = timedelta_obj.days
            if day > 0:
                insert_in_Local(get_htmlSource, SegField)
            else:
                print("Expired Tender")
                Global_var.expired += 1
        else:
            print("Deadline Not Given")
            Global_var.deadline_Not_given += 1
    except Exception as e:
        exc_type , exc_obj , exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname , "\n" ,exc_tb.tb_lineno)