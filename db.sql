create table if not exists luvio.user_accounts (
    id bigserial PRIMARY KEY,
    renter_profile_id bigserial FOREIGN KEY,
    agent_profile_id bigserial FOREIGN KEY,
    landlord_profile_id bigserial FOREIGN KEY,
    username varchar(255),
    password_hashed varchar(200), -- https://auth0.com/blog/adding-salt-to-hashing-a-better-way-to-store-passwords/
    password_salt varchar(20),
    first_name varchar(100),
    last_name varchar(100),
    date_of_birth date,
    primary_email varchar(320), -- https://stackoverflow.com/questions/386294/what-is-the-maximum-length-of-a-valid-email-address
    secondary_email varchar(320),
    mobile varchar(10),
)

-- Relationships:

"""

  profile types
- renter can only specify living address(es)
- agents can only specify managed addresses(es)
- landlords can specify both living or managed address(es)

  1 account -< profiles
- 1 account can have multiple profiles
- e.g an account can have renter profile, but also landlord profile or agent profile
- 1 account can only have 1 profile for each type

  1 address >-< profiles
- 1 address can be linked to many profiles
- AND 1 profile can be linked to many address
- e.g one or multiple renters can have history to an address (live together), an agent can also be managing an address, a landlord can own multiple addresses
- e.g a renter can have >1 entries in address history, an agent can manage multiple addresses



"""

"""
things inside a profile
- (come from account) first name last name
- avatar link
- (come from account) account_id -> foreign key
- profile type                  -> foregin key renter? agent? landlord? maybe an enum
- (come from employment history below) job title and company
- (come from account) date of birth
- (come from account) mobile number
- profile_pitch
- address_history               -> might be another table referecing profile id as foreign key (1 profile can have many addresses), to include info like move in and move out dates, whether they own the property or not, which is the current address, has this address been reference checked? what's the email and mobile and profile id (if existed) of the referee
- employment_history            -> same for address
- income_source                 -> also another table, income type, pay frequency, amount after tax per frequency, amount per month, amount per year, proof of income
- identity                      -> also another table, id type, id number, expiry date, proof of id
- emergency_contact             -> another table, full name, relationship, mobile, email, profile id (if existed)
- endorsements                  -> another table, profile id of endorser, endorse content/message, for which address, relationship with endorser, endorsed date
- profile_url                   -> unique url for each profile, can be easily shared (maybe a tinyurl as well)
"""