from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item
from .models import Conversation
from .forms import ConversationMessageForm

@login_required
def new_conversation(request, item_pk):
    item= get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('dashboard:index')
    
    # get all the conversations related to the item mentioned above
    conversations= Conversation.objects.filter(item= item).filter(member__in= [request.user.id])

    # to check whether, if there was already a conversation started between you and the owner
    # then redirect to the conversations
    if conversations:
        # redirect to conversations
        return redirect('conversation:detail', pk= conversations.first().id)

    if request.method== "POST":
        form= ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation= Conversation.objects.create(item=item)    #to create a new conversation
            conversation.member.add(request.user)
            conversation.member.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation= conversation
            conversation_message.created_by= request.user
            conversation_message.save()

            return redirect ('item:detail', pk= item_pk)
    else:
        form = ConversationMessageForm()

    return render( request, 'conversation/new.html',{
        'form': form
    })

@login_required
def inbox(request):
    # to get all the conversations that you are a member of
    conversations= Conversation.objects.filter(member__in= [request.user.id])

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })

@login_required
def detail(request, pk):
    conversation= Conversation.objects.filter(member__in= [request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form= ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message= form.save(commit= False)      #if form is valid, creating a new conversation message.
            conversation_message.conversation= conversation     # linking this message to conversation created above
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()     #to update the modified date of conversation 

            return redirect('conversation:detail', pk= pk)
        
    else:
        form= ConversationMessageForm()


    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form,
    })