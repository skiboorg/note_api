from django.urls import path,include
from . import views

urlpatterns = [


    path('me', views.GetUser.as_view()),
    path('update', views.UpdateUser.as_view()),
    path('check12', views.CheckWallet.as_view()),
    path('check-wallet', views.CheckWalletWl.as_view()),
    path('mint', views.Mintt.as_view()),
    path('cr_tx_id', views.CrTxId.as_view()),
    path('send', views.Send.as_view()),
    path('claim', views.Claim.as_view()),
    path('claim_upgrades', views.ClaimUpgrades.as_view()),
    path('coin_upgrades', views.CoinUpgrades.as_view()),
    path('recovery', views.SaveForm.as_view()),
    path('tx_history', views.TxHistory.as_view()),
    path('test', views.Test.as_view()),
    path('buy_upgrade', views.BuyUpgrade.as_view()),
]
