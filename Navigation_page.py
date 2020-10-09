from selenium import webdriver
import time
import html
import sys, os
from datetime import datetime,timedelta
import Global_var
import wx
import string
import re
import string
from Scraping_things import scrap_data
app = wx.App()

def chormedriver():
    browser = webdriver.Chrome(executable_path=str(f"C:\\chromedriver.exe"))
    browser.get('https://www.tenderwizard.my/')
    browser.maximize_window()
    time.sleep(8)
    get_links(browser)

def get_links(browser):
    links_list = []
    for links in browser.find_elements_by_xpath('//*[@class="hm_pg_list"]/li/a'):
        links_list.append(links.get_attribute('href'))

    for link in links_list:
        error = True
        while error == True:
            try:
                browser.get(link)
                time.sleep(5)
                try:
                    for close_tooltip in browser.find_elements_by_xpath("//*[@class='fa fa-times cst-icon-2']"):
                        close_tooltip.click()
                        break
                except:pass
                pos = [] #list to store positions for each 'char' in 'string'
                for n in range(len(link)):
                    if link[n] == '/':
                        pos.append(n)
                purchaser_name = link[pos[-1]:]
                purchaser_name = purchaser_name.replace('/','')
                custom_tender_link = f'https://www.tenderwizard.my/ROOTAPP/tenderfreeview.jsp?company={purchaser_name}'
                browser.get(custom_tender_link)
                time.sleep(3)
                tender_links_list = []
                inthere = True
                page_no = 1
                for next_page in browser.find_elements_by_xpath("//*[@class='pagination']/tbody/tr/td"):
                    for get_links in browser.find_elements_by_xpath("//*[@class='tblsummary']/tbody/tr/td[5]/a"):
                        get_links = get_links.get_attribute('href')
                        get_links =  get_links.partition("('")[2].partition("');")[0]
                        main_tender_link = f"https://www.tenderwizard.my/ROOTAPP/{get_links}"
                        tender_links_list.append(main_tender_link)
                        inthere = False
                    if page_no != 1:
                        browser.get(f'https://www.tenderwizard.my/ROOTAPP/NewTenderFreeView.jsp?&ymns={str(page_no)}&ymnsl=1&iPageStart=2&iStart=1&col1=&col2=&col3=&col4=&col5=&col6=&col7=&')
                        time.sleep(2)
                    page_no += 1
                if inthere == True:
                        # wx.MessageBox(' Nothing there to collect link ','tenderwizard.my', wx.OK | wx.ICON_INFORMATION)
                        time.sleep(1)
                else:
                    for tender_link in tender_links_list:
                        browser.get(tender_link)
                        time.sleep(3)
                        get_htmlsource = ''
                        for purchaser_tbl in browser.find_elements_by_xpath("//*[@class='info']"):
                            purchaser_tbl = purchaser_tbl.get_attribute('outerHTML')
                            purchaser_tbl = re.sub(' +', ' ', str(purchaser_tbl))
                            purchaser_tbl = html.unescape(str(purchaser_tbl))
                            get_htmlsource += purchaser_tbl.replace('-\t','').replace('-\n','').replace('\t','').replace('\n','')
                            break
                        for tenderDetail in browser.find_elements_by_xpath('//*[@id="tenderDetail"]'):
                            tenderDetail = tenderDetail.get_attribute('outerHTML')
                            tenderDetail = re.sub(' +', ' ', str(tenderDetail))
                            tenderDetail = html.unescape(str(tenderDetail))
                            get_htmlsource +=tenderDetail.replace('-\t','').replace('-\n','').replace('\t','').replace('\n','')
                            break
                        if get_htmlsource == '':
                                wx.MessageBox(' get_htmlsource Blank ','tenderwizard.my', wx.OK | wx.ICON_INFORMATION)
                        else:
                            scrap_data(browser,get_htmlsource,tender_link)
                            Global_var.Total += 1
                            print(f'Total: {str(Global_var.Total)} Deadline Not given: {Global_var.deadline_Not_given} duplicate: {Global_var.duplicate} inserted: {Global_var.inserted} expired: {Global_var.expired} QC Tenders: {Global_var.QC_Tenders}')
                error = False
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",exc_tb.tb_lineno)
                error = True
                time.sleep(5)
    wx.MessageBox(f'Total: {str(Global_var.Total)}\nDeadline Not given: {Global_var.deadline_Not_given}\nduplicate: {Global_var.duplicate}\ninserted: {Global_var.inserted}\nexpired: {Global_var.expired}\nQC Tenders: {Global_var.QC_Tenders}','tenderwizard.my', wx.OK | wx.ICON_INFORMATION)
    browser.close()
    sys.exit()
chormedriver()