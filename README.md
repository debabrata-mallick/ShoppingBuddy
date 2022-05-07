# ShoppingBuddy

Debabrata Mallick (203051004 - debabrata)



Steps to install and run:

Flask Server:
1. Create Python virtual environment and activate it:
    a.  python3 -m venv venv
    b.  Activate for windows: 
            venv\Scripts\activate
        Activate for Linux:
            . venv/bin/activate

2. Install packages 
    a. pip install flask
    b. pip install requests
    c. pip install beautifulsoup4
    d. pip install flask-cors 
    e. pip install pandas
    *. pip install lxml (Optional, check errors section)
    Or refer requirements.txt

3. cd ShoppingBuddy
4. For PowerShell, run:
       $env:FLASK_APP="ShoppingBuddyAPI"
   For Linux, run:
       export FLASK_APP="ShoppingBuddyAPI"
5. For PowerShell, run:
       $env:FLASK_ENV="developoment"
   For Linux, run:
       export FLASK_ENV="developoment"

6. flask run

Frontend:
7. Open following webpage in browser: ShoppingBuddy/ShoppingBuddyUI/index.html


For testing API (e.g. in Postman)
=============================================
URL: http://127.0.0.1:5000/compare/
Method: POST
header: Content-Type='application/json'
Body:
{
    "urls":[
        "https://www.amazon.in/Bravo-15-A4DDR-023-Enthusiast-Notebook/dp/B086L7CMC9",
        "https://www.amazon.in/HP-du2069TU-15-6-inch-Laptop-i3-1005G1/dp/B087S3FPDG/ref=sr_1_8?dchild=1&keywords=laptop&qid=1604481107&sr=8-8",
        "https://www.flipkart.com/msi-bravo-15-ryzen-5-hexa-core-4600h-16-gb-512-gb-ssd-windows-10-home-4-graphics-amd-radeon-rx-5500m-a4ddr-208in-gaming-laptop/p/itm878509049b9a9?pid=COMFTYB3JHQQ2HBP&lid=LSTCOMFTYB3JHQQ2HBPMFUXWU&marketplace=FLIPKART&srno=b_1_1&otracker=hp_omu_Top%2BOffers_2_3.dealCard.OMU_3NKBT44WP7VE_3&otracker1=hp_omu_PINNED_neo%2Fmerchandising_Top%2BOffers_NA_dealCard_cc_2_NA_view-all_3&fm=organic&iid=en_%2FuggwikoJ94abjZgfVjec9qtdlRhWh4PzejizXCtwp9vsCQ9NB1rDaWBn%2BzZ0kKSp%2Fja3VgU%2Fi9aYXW1EMVKcg%3D%3D&ssid=ex476uw75s0000001604487536545"
    ],
    "category":"laptop"
}


Possible Errors and fixes you may face
=====================================
1. If you are running from vscode and get error:
   RuntimeError: The current Numpy installation fails to pass a sanity check due to a bug in the windows runtime. See this issue for more information: https://tinyurl.com/y3dm3h86
   Install earlier version of numpy (https://stackoverflow.com/questions/64729944/):
   pip install numpy==1.19.3

2. If you get following error:
   bs4.FeatureNotFound: Couldn't find a tree builder with the features you requested: lxml. Do you need to install a parser library?
   Install lxml:
   pip install lxml 


Note: We have tested the application in Windows 10 Home.


References:
https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/
https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_singleton.htm
