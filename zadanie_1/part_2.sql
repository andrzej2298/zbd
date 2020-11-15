select
    contacts.day as dzien,
    targets.id - 1 as grupa,
    ads.name as reklama,
    count(distinct users.id) as osob
from contacts
join users
on users.id = contacts.user_id
join ads
on ads.id = contacts.ad_id
join demography
on demography.day = contacts.day
and demography.user_id = users.id
join targets
on demography.demography like replace(targets.definition, ' ', '_')
group by contacts.day, targets.id, ads.name;
