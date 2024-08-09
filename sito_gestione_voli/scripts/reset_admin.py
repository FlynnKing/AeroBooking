from django.contrib.auth.models import User

def run():
    # Configura le nuove credenziali
    nuovo_nome_utente = 'admin'
    nuova_password = 'pass'
    nuova_email = ''

    # Trova o crea l'utente amministratore
    user, created = User.objects.get_or_create(username=nuovo_nome_utente)
    
    # Aggiorna le informazioni dell'utente
    user.set_password(nuova_password)
    user.email = nuova_email
    user.is_superuser = True
    user.is_staff = True
    user.save()

    if created:
        print(f"Creato nuovo superuser: {nuovo_nome_utente}")
    else:
        print(f"Superuser aggiornato: {nuovo_nome_utente}")
