% Import testpathces.csv: first column as cell array and rename the variable as testpatches
% Second column as cell array and rename the variable as predictedLabelstxt 
% Third to 25th columns as a numeric array and rename the variable as scoresori
species_list={'empty','deer','moose','squirrel','rodent','small_mammal','elk','prongs','rabbit','bighorn_sheep',...
    'fox','coyote','black_bear','raccoon','skunk','wolf','bobcat','cat','dog','opossum','bison','mountain_goat',...
    'mountain_lion'};
predictedLabels=predictedLabelstxt;
for spe=1:length(species_list)
    predictedLabels=replace(predictedLabels,species_list{spe},num2str(spe-1));
end
%
for spe=1:length(species_list)
    Match=cellfun(@(x) ismember(x, {species_list{spe}}), predictedLabelstxt, 'UniformOutput', 0);
    r=find(cell2mat(Match));
    [val,ind]=max(scoresori(r(1),:));
    scores(:,spe)=scoresori(:,ind);
end

testpatches=replace(testpatches,'data/test/all/','');
testpatchesT=cell2table(testpatches);
testpatches=testpatchesT.testpatches2;
testpatches=(strtok(testpatches,'_'));
testpatches=replace(testpatches,'.jpg','');
[C,ia,ic] = unique(testpatches);
%%%%%%%%%%%%Import testseq.txt as cell array
testseq=replace(testseq,'F:\Datasets\iWildCam_IDFG\iWildCam_IDFG_Sequences_Merge_fg_patches_images_299\','');
testseq=split(testseq,'\');
testseqT=cell2table(testseq);
seqid=testseqT.testseq1;
imid=testseqT.testseq2;
imid=replace(imid,'.jpg','');
imid=strtok(imid,'_');
[C1,ia1,ib1] =intersect(imid,testpatches);

[C2,ia2,ic2] = unique(seqid);
[C3,ia3,ic3] = unique(imid);

imid2=replace(imid,'.jpg','');
imid2=strtok(imid2,'_');
[C5,ia5,ic5] = unique(imid2);


imindex=0;labelstest=[];
for i=1:length(C2)
    patchID=find(ic2==i);
    patchID2=patchID;
    for jj=1:length(patchID)
        patchID2(jj)=ib1((ic3(patchID(jj))));
    end
    %intersect(patchID2,ic4)
    Slabeltsssst=str2num(char(predictedLabels{patchID2}));
    Mac=sum(scores(patchID2,:),1);
    Mac=Mac(2:end);
    [val,Mac]=max(Mac);
    SlScores=max(scores(patchID2,:),[],2);
    Slabeltsssst=Mac;
    imIDs=unique(ic5(patchID));
    for j=1:length(imIDs)
        imindex=imindex+1;
        %C5{imIDs(j)}
        id{imindex}=C5{imIDs(j)};
        patchind=ib1(ic3(find(ic5==imIDs(j))));
        labeltsssst=str2num(char(predictedLabels{ib1(ic3(find(ic5==imIDs(j))))}));
        ilscores=[];illabel=[];pind=0;
        for P=1:length(labeltsssst)
        
        ilscores(P)=max(scores(patchind(P),:));
        if ilscores(P)>0.8&&labeltsssst(P)==0
        illabel(P)=0;
        else
             illabel(P)=Slabeltsssst;
        end
        end
        illabel=illabel(illabel~=0);
            if ~isempty(illabel)
                
                labelstest(imindex)=Slabeltsssst;
            else
               
                labelstest(imindex)=0;
            end
    end
end
% Images with no foreground patches from background subtraction are
% classified as empty
Cmiss=setdiff(C,C5);
for i=139262:153730
   labelstest(i)=0;
   id{i}=Cmiss{i-139261};
   
end
 mypredictions.id=images;
mypredictions.predicted=vote;
T = struct2table(mypredictions);
 writetable(T,'BXVT_SL.csv')