---
game: ref_estate__shipped
model: gpt-mini
condition: win
seed: 0
round: 1
chars: 950
---
When I land on an unowned property, I buy it if its price is less than or equal to my cash minus my reserve; otherwise I do not buy.  
When I pass START, I collect the salary immediately and add it to my balance.  
When I land on another investor's property, I pay the full rent immediately and deduct it from my balance.  
When I land on my own property, I do nothing and leave my balance unchanged.  
When a purchase is made, I record the payment to the bank and the new balance immediately.  
When I pay rent to another investor, I record the payment to that investor and the new balance immediately.  
When asked to declare, I always output the payment token, a yes/no buy decision, and my updated balance.  
I keep a cash reserve of 50 and never buy a property that would leave me with less than this reserve; buying down to very low cash proved harmful.  
If I cannot afford an offered property at all, I explicitly decline and make no payment.