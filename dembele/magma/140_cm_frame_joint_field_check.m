// D75: independent joint-reconstruction and coefficient-box checks.
SetQuitOnError(true); SetColumns(0); SetSeed(75);
started:=Cputime();
load "dembele/data/computed/cm_frame_joint_field_data.m";
load "dembele/data/computed/cm_frame_denominator_space_coordinates.m";
m:=31^joint_training_digits; M:=31^joint_validation_digits;
Z:=Integers(M); Q:=Rationals(); T<t>:=PolynomialRing(Q);
f:=T!joint_field_polynomial; F<theta>:=NumberField(f);
assert #joint_trials eq 9 and #joint_targets eq 9;
assert Sort([Integers()!v[1] mod 31:v in joint_trials[2..9]]) eq [4,9,10,11,20,21,22,27];
function FieldVector(row,theta)
    return [&+[row[8*(i-1)+j]*theta^(j-1):j in [1..8]]:i in [1..17]];
end function;
for index in [1..#joint_trials] do
    trial:=joint_trials[index]; root:=trial[1]; anchor:=trial[2];
    R:=Matrix(Integers(),trial[3]); target:=[Z!x:x in joint_targets[index]];
    assert Nrows(R) eq 136 and Ncols(R) eq 136;
    assert Numerator(Evaluate(f,root)) mod M eq 0;
    assert Integers()!target[anchor] mod 31 ne 0;
    if index gt 1 then assert joint_targets[index] eq space_denominator_coordinates; end if;
    assert Abs(Determinant(R)) eq m^16;
    inverse:=m*ChangeRing(R,Q)^-1;
    assert &and[Denominator(x) eq 1:x in Eltseq(inverse)];
    D:=ChangeRing(inverse,Integers());
    assert R*D eq m*IdentityMatrix(Integers(),136);
    S:=Maximum([&+[Abs(D[i,j]):i in [1..136]]:j in [1..136]]);
    H:=(m-1) div S;
    assert S eq trial[6] and H eq trial[7];
    assert H*S lt m and (H+1)*S ge m;
    powers:=[(Z!root)^(j-1):j in [1..8]];
    matching:=[]; survivors:=[]; values:=[];
    for rowindex in [1..136] do
        row:=Eltseq(R[rowindex]);
        value:=[&+[row[8*(i-1)+j]*powers[j]:j in [1..8]]:i in [1..17]];
        Append(~values,value);
        residual:=[Integers()!(value[i]*target[anchor]-value[anchor]*target[i]):i in [1..17]|i ne anchor];
        assert &and[x mod m eq 0:x in residual];
        if Integers()!value[anchor] mod 31 eq 0 then
            Append(~matching,-1);
        else
            v:=Minimum([x eq 0 select joint_validation_digits else Valuation(x,31):x in residual]);
            Append(~matching,v);
            if v eq joint_validation_digits then Append(~survivors,rowindex); end if;
        end if;
    end for;
    assert matching eq trial[4];
    assert survivors eq trial[5];
    if index eq 1 then
        known:=[&+[joint_control_coefficients[i][j]*theta^(j-1):j in [1..8]]:i in [1..17]];
        known_values:=[&+[joint_control_coefficients[i][j]*powers[j]:j in [1..8]]:i in [1..17]];
        assert target eq [x/known_values[anchor]:x in known_values];
        assert #survivors gt 0;
        for rowindex in survivors do
            exact:=FieldVector(Eltseq(R[rowindex]),theta);
            assert exact[anchor] ne 0;
            assert &and[exact[i]*known[anchor] eq exact[anchor]*known[i]:i in [1..17]];
        end for;
        changed:=target; changed[joint_negative_coordinate]+:=m;
        for rowindex in [1..136] do
            value:=values[rowindex];
            if Integers()!value[anchor] mod 31 ne 0 then
                assert exists{i:i in [1..17]|value[i]*changed[anchor] ne value[anchor]*changed[i]};
            end if;
        end for;
        print "PASS|JOINT_EXACT_F_CONTROL_AND_UNUSED_DIGIT_REJECTION";
    end if;
    printf "JOINT_TRIAL|%o|ROOT|%o|SURVIVORS|%o|EXCLUDED_BOX|%o\n",index,root mod 31,#survivors,H;
end for;
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|140_CM_FRAME_JOINT_FIELD_CHECK";
quit;
