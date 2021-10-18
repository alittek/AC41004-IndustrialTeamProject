# AC41004-IndustrialTeamProject

- Alina Littek - 180016182
- Bjarne Kopplin - 180016866
- Mikolaj Olejnik - 180006025
- Scott Fulton - 180009413
- Alan Sunny - 160009235
- Fergus McLaughlin - 170015911
- Godfrey Morewood - 170018315
- Patrizio Pigliacelli - 190014172

# Installation
Download an install Virtual Box and [Vagrant](https://www.vagrantup.com/downloads).

# Run the code
Clone the repository and run the following commands from the root folder of the repository.
```bash
vagrant up
vagrant ssh
```
The above commands might take a while because an update is made the first time the vagrant box is brought up. You should now be inside the vagrant box.
```bash
cd /vagrant/theohealth
python3 manage.py migrate
python3 manage.py runserver 0:9000
```
You can now access the server at `localhost:9000` on the guest machine.
