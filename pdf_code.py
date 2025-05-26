from fpdf import FPDF
import pandas as pd


class Articles:

    def __init__(self):
        self.df = None

    def get_articles(self):
        """ Read the csv file using pandas"""
        self.df = pd.read_csv('articles.csv')
        return self.df

    def price_name(self, id):
        """Retrieve the name and price of the items"""
        # Check if the id exists
        id_exists = self.df['id'].isin([id]).any()

        if id_exists:
            item_name = self.df.loc[self.df["id"] == id, "name"].squeeze()
            item_price = self.df.loc[self.df["id"] == id, "price"].squeeze()
            return item_name, item_price
        else:
            return None, None


class Receipt(FPDF):
    def __init__(self, id, name, price):
        super().__init__()
        self.name = name
        self.price = price
        self.id = id


    def generate_receipt(self):
        self.add_page()

        self.set_font(family="Times", size=16, style="B")
        self.cell(w=50, h=8, txt=f"Receipt nr.{self.id}", ln=1)

        self.set_font(family="Times", size=16, style="B")
        self.cell(w=50, h=8, txt=f"Article: {self.name}", ln=1)

        self.set_font(family="Times", size=16, style="B")
        self.cell(w=50, h=8, txt=f"Price: {self.price}", ln=1)

        self.output("receipt.pdf")


# Instantiate an article class
article = Articles()
print(article.get_articles().head())

# Get Article ID to buy
article_id = int(input("Choose an article to buy: "))
article_name, article_price = article.price_name(article_id)

# Generate receipt if article exists
if article_name is not None:
    # Generate Receipt
    receipt = Receipt(article_id, article_name, article_price)
    receipt.generate_receipt()
else:
    print("Article item does not exist.")

