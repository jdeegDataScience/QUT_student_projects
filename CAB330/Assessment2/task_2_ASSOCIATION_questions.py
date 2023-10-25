# load dataset
pos_data = pd.read_csv('POS_TRANS_v1.csv', na_filter=False, low_memory=False)

# load packages
from apyori import apriori

# 2.1 - Data Prep
pos_df = preprocess_pos_data(pos_data)

# ---

# 2.2 - Variables included in analysis
pos_df.columns

# ---

# 2.3 - Association Mining
# separate cell to define function 
def convert_apriori_results_to_pandas_df(results):
    rules = []

    for rule_set in results:
        for rule in rule_set.ordered_statistics:
            # items_base = left side of rules, items_add = right side
            # support, confidence and lift for respective rules
            rules.append([','.join(rule.items_base),
                          ','.join(rule.items_add),
                          rule_set.support,
                          rule.confidence, rule.lift])
    
    # typecast it to pandas df
    return pd.DataFrame(rules, columns=['Left_side', 'Right_side',
                                        'Support','Confidence', 'Lift'])

# run apriori and use the defined function to generate a df of the results
transactions = pos_df.groupby(['Transaction_Id'])['Product_Name'].apply(list)
# type cast the transactions from pandas into normal list format
# run apriori
transaction_list = list(transactions)
results = list(apriori(transaction_list, min_support=0.01,
                      min_confidence=0.3))

result_df = convert_apriori_results_to_pandas_df(results)

# ---

# 2.3.a - Rule with highest lift value
# sort all acquired rules descending by lift
desc_lift = result_df.sort_values(by='Lift', ascending=False)
print(desc_lift.head(10))

# ---

# 2.3.b - Rule with highest confidence value
# sort all acquired rules descending by confidence
desc_conf = result_df.sort_values(by='Confidence', ascending=False)
print(desc_conf.head(10))

# ---

# 2.4 - Confidence, lift, and support plots 
# Mary?

# ---

# 2.5 - Tea Rules
# Filter the association rules to include only rules with 'Tea' on the left side
tea_rules = result_df[result_df.Left_side.str.contains('Tea')]

# ---

# 2.5.a - Number of tea rules
# Count the number of rules in the subset
num_tea_rules = len(tea_rules)
print(f"There are {num_tea_rules} rules with 'Tea' on the left side.")

# ---

# 2.5.b - Interpret: products customers are likely to purchase if they're also purchasing tea
# slice for rules with high confidence
conf_threshold = 0.3

top_tea_rules = tea_rules[tea_rules.Confidence > conf_threshold]

# filter for rules with positive correlation
top_tea_rules = top_tea_rules[top_tea_rules.Lift > 1]

# Sort the rules within the subset by confidence in descending order
top_tea_rules.sort_values(by='Confidence', ascending=False, inplace=True)

# reset index to enable FOR loop
top_tea_rules.reset_index(drop=True, inplace=True)

# initialise empty list for products
tea_top_products = []

# record each UNIQUE individual item
for RHS_prods in range(len(top_tea_rules.Right_side)):
    # if the RHS contains only multiple items
    if ',' in top_tea_rules.Right_side[RHS_prods]:
        # split into array of each item
        current_prods = top_tea_rules.Right_side[RHS_prods].split(',')
        # cycle through products and add to list if not already present
        for prod in current_prods:
            if prod not in tea_top_products:
                tea_top_products.append(prod)
    # only one RHS product in rule; add to list if not already present
    elif top_tea_rules.Right_side[RHS_prods] not in tea_top_products:
        tea_top_products.append(top_tea_rules.Right_side[RHS_prods])

# Print the top products
print(f"More than {conf_threshold:.0%} of customers who purchased Tea also purchased:")
for product in tea_top_products:
    print(f"- {product}")

# ---

# 2.6 - Products to boost Shampoo sales, i.e. Shampoo on RHS with high lift.
# Filter the association rules to include only rules with 'Shampoo' on RHS
shampoo_rules = result_df[result_df.Right_side.str.contains('Shampoo')]

# filter for rules with positive correlation
shampoo_rules = shampoo_rules[shampoo_rules.Lift > 1]

# Sort the rules within the subset by lift in descending order
shampoo_rules.sort_values(by='Lift', ascending=False, inplace=True)

# reset index to enable FOR loop
shampoo_rules.reset_index(drop=True, inplace=True)

# initialise empty list for products
shampoo_boosters = []

# record each UNIQUE individual item
for LHS_prods in range(len(shampoo_rules.Left_side)):
    # if the LHS contains multiple items
    if ',' in shampoo_rules.Left_side[LHS_prods]:
        # split into array of each item
        current_prods = shampoo_rules.Left_side[LHS_prods].split(',')
        # cycle through products and add to list if not already present
        for prod in current_prods:
            if prod not in shampoo_boosters:
                shampoo_boosters.append(prod)
    # only one LHS product in rule; add to list if not already present
    elif shampoo_rules.Left_side[LHS_prods] not in shampoo_boosters:
        shampoo_boosters.append(shampoo_rules.Left_side[LHS_prods])

# Print the top products
print(f"Customers were at least {min(shampoo_rules.Lift):.2} times as likely to purchase Shampoo if they were purchasing any combination of these products:")
for product in shampoo_boosters:
    print(f"- {product}")
