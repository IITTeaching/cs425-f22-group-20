insert into Branch (branchID, address, overdraftFee, monthlyFee, waiveFeeMin)
values  ('10000000-0000-4000-A000-000000000000', '1234 N. Quasar Blvd.', 2, 55, 4000),
        ('20000000-0000-4000-A000-000000000000', '5432 E. Jammin Rd.', 3, 20, 10000),
        ('30000000-0000-4000-A000-000000000000', '8888 S. EEL Ave.', 1, 9, 600);


insert into Employee (ssn, emp_name, emp_role, address, salary, branch)
values  ('555', 'Man', 'manager', 'here', 400000, '10000000-0000-4000-A000-000000000000');

insert into Customer (ssn, name, address, branch)
values  ('123', 'Sitio', '12 S. Jenkins', '10000000-0000-4000-A000-000000000000'),
        ('456', 'Georg', '0 E. There St', '20000000-0000-4000-A000-000000000000');

insert into Account (accountNumber, balance)
values  ('10000000-0000-4000-A000-000000000000', 5),
        ('20000000-0000-4000-A000-000000000000', 0),
        ('30000000-0000-4000-A000-000000000000', 20);

insert into Holds (ssn, accountNumber)
values  ('123', '10000000-0000-4000-A000-000000000000'),
        ('456', '20000000-0000-4000-A000-000000000000'),
        ('456', '30000000-0000-4000-A000-000000000000');